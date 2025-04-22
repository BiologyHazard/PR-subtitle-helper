# 半角句号“.”在中文中一般作为小数点，因此保留半角句号。
to_newline_characters = "，。；：！？…,;:!?"
to_full_width_space_characters = "\t、/—「」『』〈〉《》【】“”‘’"
to_half_width_space_characters = "'\""

# 字幕最短宽度（中文字算 2 宽度，英文字算 1 宽度），若小于此宽度，会给出提醒，设置为 0 以禁用检查
min_width = 10
# 字幕最大宽度（中文字算 2 宽度，英文字算 1 宽度），若大于此宽度，会给出提醒，设置为 float("inf") 以禁用检查
max_width = 40
