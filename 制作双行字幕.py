import srt


def convert_to_double_line(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        subtitles = list(srt.parse(f.read()))

    # 加一个空行，方便处理
    subtitles.append(srt.Subtitle(
        index=0,  # 任意值
        start=0,
        end=0,
        content=" "
    ))

    new_subtitles = []
    for i, subtitle in enumerate(subtitles[:-1]):
        if i % 2 == 0:
            new_content = f"→  {subtitles[i].content}  ←\n{subtitles[i+1].content}"
        else:
            new_content = f"{subtitles[i+1].content}\n→  {subtitles[i].content}  ←"

        new_subtitle = srt.Subtitle(
            index=subtitle.index,
            start=subtitle.start,
            end=subtitle.end,
            content=new_content
        )
        new_subtitles.append(new_subtitle)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(srt.compose(new_subtitles))


if __name__ == "__main__":
    input_file = "双行字幕输入.srt"
    output_file = "双行字幕输出.srt"
    convert_to_double_line(input_file, output_file)
