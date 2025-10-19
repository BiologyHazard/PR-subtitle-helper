from pathlib import Path

import srt

input_path = Path("双行字幕输入.srt")
output_path = Path("双行字幕输出.srt")


def convert_to_double_line(input_text) -> str:
    subtitles = list(srt.parse(input_text))

    # 加一个空行，方便处理
    subtitles.append(
        srt.Subtitle(
            index=0,  # 任意值
            start=0,
            end=0,
            content=" ",
        )
    )

    new_subtitles = []
    for i, subtitle in enumerate(subtitles[:-1]):
        if i % 2 == 0:
            new_content = f"→  {subtitles[i].content}  ←\n{subtitles[i + 1].content}"
        else:
            new_content = f"{subtitles[i + 1].content}\n→  {subtitles[i].content}  ←"

        new_subtitle = srt.Subtitle(
            index=subtitle.index,
            start=subtitle.start,
            end=subtitle.end,
            content=new_content,
        )
        new_subtitles.append(new_subtitle)

    return srt.compose(new_subtitles)


def main():
    input_srt = input_path.read_text("utf-8")
    output_srt = convert_to_double_line(input_srt)
    output_path.write_text(output_srt, "utf-8")


if __name__ == "__main__":
    main()
