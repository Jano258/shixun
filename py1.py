import os
import chardet


def convert_txt_to_utf8(directory):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.txt'):
                file_path = os.path.join(root, filename)

                # 使用chardet检测文件编码
                with open(file_path, 'rb') as file:
                    result = chardet.detect(file.read())
                    original_encoding = result['encoding']

                # 确保检测到了编码才进行转换
                if original_encoding:
                    print(f"正在转换: {file_path}")

                    # 读取并转换编码
                    with open(file_path, 'r', encoding=original_encoding) as file:
                        content = file.read()

                    # 写入UTF-8编码的新文件，先创建一个临时文件名以免直接覆盖原文件
                    temp_file_path = file_path + '.tmp'
                    with open(temp_file_path, 'w', encoding='utf-8') as file:
                        file.write(content)

                    # 替换原文件
                    os.replace(temp_file_path, file_path)
                else:
                    print(f"未检测到编码，跳过文件: {file_path}")


# 指定要转换的目录
directory_path = './data2'
convert_txt_to_utf8(directory_path)
print("所有txt文件编码转换完成。")