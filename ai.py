import json
from openai import AsyncOpenAI
from pyrogram.types import Message
import asyncio


class AIResponseError(Exception):
    pass


class AIResponseResult:
    def __init__(self, possibility: int, token_used: int):
        self.possibility = possibility
        self.token_used = token_used

    def __str__(self):
        return f"possibility: {self.possibility}, token_used: {self.token_used}"


async def chk_message(message: Message, api_key, max_token, image_url: "") -> AIResponseResult:
    prompt = """You are an advanced spam detection system for a Telegram chat. Your task is to analyze the user's `username`, `bio`, and `message` to determine the likelihood that the user is a spammer. You should output a number from 0 to 100, where 0 indicates the user is definitely not a spammer, and 100 indicates the user is definitely a spammer.

Consider the following factors: 

- The inclusion of suspicious links.

- The overall tone and context of the message (e.g., overly promotional, using excessive emojis or symbols). 

- The presence of pornographic or inappropriate content in the message or images.

Based on these factors, provide a spam likelihood score for the given user information. 

**Your response must be a single number between 0 and 100. Do not include any additional text or explanation.**

Example input: { "username": "安全洗U赚差价1U换1.5U", "bio": "公群交易，洗U赚差价，黑U承兑，已上押《8888U》VIP群上押《20000U》公群已平稳运行半年多，欢迎进公群了解 https://t.m", "message": "我来了😂😂" } Example output: 100"""
    client = AsyncOpenAI(api_key=api_key)
    if message.from_user is None:
        user_name = str(message.chat.title)
        bio = str(message.chat.description)
    else:
        user_name = str(message.from_user.first_name) + " " + str(message.from_user.last_name)
        bio = str(message.chat.bio)
    # bio = ""  # bio 需要通过 get_chat 获取, 暂时不使用
    text = {
        "username": user_name,
        "bio": bio,
        "message": message.text
    }
    print(json.dumps(text, ensure_ascii=False))
    content = []
    if text != "":
        content.append({
            "type": "text",
            "text": json.dumps(text)
        })
    if image_url != "":
        content.append({
            "type": "image_url",
            "image_url": {
                "url": image_url
            }
        })
    chat_completion = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            },
            {
                "role": "user",
                "content": content
            }
        ],
        temperature=0,
        max_tokens=512,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    token_used = chat_completion.usage.total_tokens
    result = chat_completion.choices[0].message.content
    try:
        return AIResponseResult(possibility=int(result), token_used=token_used)
    except Exception as e:
        raise AIResponseError(f"Invalid response from AI: {result}") from e
