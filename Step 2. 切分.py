from collections.abc import Generator
from pathlib import Path

from config import (
    max_width,
    min_width,
    to_full_width_space_characters,
    to_half_width_space_characters,
    to_newline_characters,
)

input_path = Path("Step 1. 文稿.txt")
output_path = Path("Step 3. 切分结果.txt")


def calc_line_width(line: str) -> int:
    """中文字算 2 宽度，英文字算 1 宽度"""
    width = 0
    for char in line:
        if "\u4e00" <= char <= "\u9fff":  # Chinese characters
            width += 2
        else:
            width += 1
    return width


def cut_text(text: str) -> Generator[str, None, None]:
    """按标点符号切分文本并标记宽度不合适的行"""
    # 把标点符号替换为换行符、全角空格和半角空格
    for character in to_newline_characters:
        text = text.replace(character, "\n")
    for character in to_half_width_space_characters:
        text = text.replace(character, " ")
    for character in to_full_width_space_characters:
        text = text.replace(character, "　")

    for line in text.splitlines():
        line = line.strip()
        # 空行不检查宽度
        if not line:
            yield line
            continue

        # 检查行宽度
        line_width = calc_line_width(line)
        # 标记宽度过长或过短的行
        if not min_width <= line_width <= max_width:
            yield f"{line}!"
        else:
            yield line


def main():
    input_content = input_path.read_text("utf-8")
    output_content = cut_text(input_content)
    with open(output_path, "w", encoding="utf-8") as file:
        file.writelines(f"{line}\n" for line in output_content)


if __name__ == "__main__":
    main()
