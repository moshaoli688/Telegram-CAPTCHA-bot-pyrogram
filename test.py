import re


def test_halal(text: str, max_halal_char_threshold: int, max_halal_pct_threshold: float) -> bool:
    # 移除空白字符（包括 \s、\uFEFF、\xA0 等）
    # 若需要移除更多类型的空白符，可自行扩展正则
    pattern = re.compile(r'[\s\uFEFF\xA0]+')
    cleaned_text = pattern.sub('', text)

    length = len(cleaned_text)
    if length == 0:
        # 根据业务逻辑决定空字符串是否视为“符合”或“不符合”
        return False

    count = 0
    for ch in cleaned_text:
        code = ord(ch)
        # 对应 JS 中的 switch(true) case 范围判断
        if (0x600 <= code <= 0x6FF or
                0x750 <= code <= 0x77F or
                0x8A0 <= code <= 0x8FF or
                0x900 <= code <= 0x97F or
                0x600 <= code <= 0x6FF or  # 原 JS 代码中重复的一段，保留
                0xA8E0 <= code <= 0xA8FF or
                0xFB50 <= code <= 0xFDFF or
                0xFE70 <= code <= 0xFEFF):
            count += 1

        # 若达到字符计数阈值，直接返回 True
        if count >= max_halal_char_threshold:
            return True

    # 若占比达到百分比阈值，也返回 True
    if (count / length) >= max_halal_pct_threshold:
        return True

    return False


# 示例调用
if __name__ == "__main__":
    test_string = "محمود سيد"
    max_char_threshold = 3
    max_pct_threshold = 0.5

    result = test_halal(test_string, max_char_threshold, max_pct_threshold)
    print("Result:", result)
