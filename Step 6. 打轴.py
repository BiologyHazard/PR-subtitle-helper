from pathlib import Path

import srt

from config import (
    extra_ignore_characters,
    to_full_width_space_characters,
    to_half_width_space_characters,
    to_newline_characters,
)

input_lines_path = Path("Step 4. 切分修改.txt")
input_srt_path = Path("Step 5. 字幕输入.srt")
output_srt_path = Path("Step 7. 字幕输出.srt")


def next_ij(i, j, input_subtitles):
    """返回下一个字符的位置"""
    if j < len(input_subtitles[i].content) - 1:
        return i, j + 1
    else:
        return i + 1, 0


def main():
    # 读取字幕输入
    input_subtitles = list(srt.parse(input_srt_path.read_text("utf-8")))
    # 预处理字幕输入
    for input_subtitle in input_subtitles:
        for character in to_newline_characters:
            input_subtitle.content = input_subtitle.content.replace(character, "\n")
        for character in to_half_width_space_characters:
            input_subtitle.content = input_subtitle.content.replace(character, " ")
        for character in to_full_width_space_characters:
            input_subtitle.content = input_subtitle.content.replace(character, "　")
        input_subtitle.content = input_subtitle.content.strip()

    output_subtitles = []
    i = 0  # 输入字幕文件的下标
    j = 0  # 输入字幕文件第i个字幕的字符位置
    for input_line in input_lines_path.read_text("utf-8").splitlines():
        input_line = input_line.strip()
        if not input_line:
            continue

        print()
        print(f"匹配: {input_line}")
        print(f"当前: {i=}, {j=}, {input_subtitles[i].content}")
        for character in input_line:
            if (
                character
                in to_newline_characters
                + to_full_width_space_characters
                + to_half_width_space_characters
                + extra_ignore_characters
            ):
                continue
            # 在字幕输入中查找字符
            while (
                input_subtitles[i].content
                and input_subtitles[i].content[j] != character
            ):
                i, j = next_ij(i, j, input_subtitles)
            # 指针移动到下一个字符
            i, j = next_ij(i, j, input_subtitles)

        # 计算时间轴
        if j == 0 and i == len(input_subtitles):
            end_time = input_subtitles[-1].end
        elif j == 0 and i < len(input_subtitles):
            end_time = (input_subtitles[i - 1].end + input_subtitles[i].start) / 2
        else:
            end_time = input_subtitles[i].start + j / len(
                input_subtitles[i].content
            ) * (input_subtitles[i].end - input_subtitles[i].start)

        if not output_subtitles:
            start_time = srt.timedelta(seconds=0)
        else:
            start_time = output_subtitles[-1].end

        output_subtitles.append(
            srt.Subtitle(
                index=0,
                start=start_time,
                end=end_time,
                content=input_line,
            )
        )

    output_srt = srt.compose(output_subtitles)
    output_srt_path.write_text(output_srt, "utf-8")


if __name__ == "__main__":
    main()
