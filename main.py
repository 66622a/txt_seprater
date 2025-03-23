import os
from charset_normalizer import from_path
from opencc import OpenCC

# 初始化 OpenCC，用于繁体转简体
cc = OpenCC('t2s')  # 't2s' 表示繁体到简体

# 定义合并后的文件名和分隔符
output_file = "merged_output.txt"
separator = "=========="

# 获取当前目录中的所有txt文件
txt_files = [f for f in os.listdir() if f.endswith('.txt') and f != output_file]

# 定义一个函数使用 charset-normalizer 检测编码
def detect_encoding(file_path):
    result = from_path(file_path).best()
    return result.encoding if result else 'latin-1'  # 默认返回 UTF-8

# 计算每个文件的字符数（包括空格和换行）用于计算进度百分比
file_lengths = {}
for txt_file in txt_files:
    encoding = detect_encoding(txt_file)  # 检测文件编码
    try:
        with open(txt_file, 'r', encoding=encoding) as infile:
            content = infile.read()
            length = len(content)
            file_lengths[txt_file] = length
    except Exception as e:
        print(f"使用编码 {encoding} 读取失败，尝试使用其他编码: {e}")
        # 尝试使用 UTF-16 和 GB2312 进行读取
        for alt_encoding in ['latin-1', 'gbk' ,'gb2312']:
            try:
                with open(txt_file, 'r', encoding=alt_encoding) as infile:
                    content = infile.read()
                    length = len(content)
                    file_lengths[txt_file] = length
                    break
            except Exception as e:
                print(f"无法使用 {alt_encoding} 读取文件 {txt_file}，错误: {e}")
                file_lengths[txt_file] = 0

# 计算总字符数和每个文件的起始百分比位置
total_length = sum(file_lengths.values())
start_percentages = {}
current_position = 0

for txt_file, length in file_lengths.items():
    start_percentages[txt_file] = (current_position / total_length * 100) if total_length > 0 else 0
    current_position += length

# 打开输出文件，写入内容并在每个文件前加入进度信息
with open(output_file, 'w', encoding='utf-8') as outfile:
    for txt_file in txt_files:
        # 写入文件的进度位置作为目录
        start_percentage = start_percentages.get(txt_file, 0)
        outfile.write(f"{separator}\n")
        outfile.write(f"文件名: {txt_file}\n")
        outfile.write(f"起始位置: {start_percentage:.2f}%\n")
        outfile.write(f"{separator}\n")

        # 写入文件内容
        encoding = detect_encoding(txt_file)  # 重新检测编码以确保正确
        content = ""
        try:
            with open(txt_file, 'r', encoding=encoding) as infile:
                content = infile.read()
        except Exception as e:
            print(f"使用编码 {encoding} 读取失败，尝试使用其他编码: {e}")
            # 尝试使用 UTF-16 和 GB2312 进行读取
            for alt_encoding in ['utf-16', 'gb2312']:
                try:
                    with open(txt_file, 'r', encoding=alt_encoding) as infile:
                        content = infile.read()
                        break
                except Exception as e:
                    print(f"无法使用 {alt_encoding} 读取文件 {txt_file}，错误: {e}")

        # 转换为简体并写入输出文件
        simplified_content = cc.convert(content)
        outfile.write(simplified_content)
        outfile.write(f"\n{separator}\n\n")  # 每个文件结束时添加分隔符和换行

print("TXT文件合并完成！")
