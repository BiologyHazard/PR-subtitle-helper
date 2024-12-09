from pathlib import Path
from collections.abc import Generator

from config import to_newline_characters, to_space_characters


input_path = Path("Step 1. 文稿.txt")
output_path = Path("Step 3. 切分结果.txt")


def cut_text(text: str) -> Generator[str, None, None]:
    for character in to_newline_characters:
        text = text.replace(character, "\n")
    for character in to_space_characters:
        text = text.replace(character, " ")

    for line in text.splitlines():
        yield line.strip()


def main():
    input_content = input_path.read_text("utf-8")
    output_content = cut_text(input_content)
    with open(output_path, "w", encoding="utf-8") as file:
        file.writelines((f"{line}\n" for line in output_content))


if __name__ == "__main__":
    main()
