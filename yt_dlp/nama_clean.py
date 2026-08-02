import os
import re


def sanitize_filename(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            old_path = os.path.join(root, name)

            # 分离文件名和后缀
            base, ext = os.path.splitext(name)

            # 1. 统一所有标点符号、特殊符号为下划线 _（保留中文字符、英文字母、数字、下划线）
            new_base = re.sub(r'[^a-zA-Z0-9_\u4e00-\u9fa5]', '_', base)

            # 2. 把当前目录名称（父目录）如果在文件名中出现过，则去掉
            parent_dir_name = os.path.basename(root)
            if parent_dir_name:
                # 对父目录名称本身也进行相同的符号清洗，以便准确匹配
                cleaned_parent = re.sub(r'[^a-zA-Z0-9_\u4e00-\u9fa5]', '_', parent_dir_name)
                cleaned_parent = re.sub(r'_+', '_', cleaned_parent).strip('_')
                if cleaned_parent and cleaned_parent in new_base:
                    new_base = new_base.replace(cleaned_parent, '')

            # 把连续的下划线合并为一个，并去除首尾多余的下划线
            new_base = re.sub(r'_+', '_', new_base)
            new_base = new_base.strip('_')

            new_name = new_base + ext
            new_path = os.path.join(root, new_name)

            if old_path != new_path:
                try:
                    os.rename(old_path, new_path)
                    print(f"Renamed: {name} -> {new_name}")
                except Exception as e:
                    print(f"Error renaming {name}: {e}")


if __name__ == '__main__':
    target_path = r"data\clean"
    if os.path.isdir(target_path):
        sanitize_filename(target_path)
        print("处理完成！")
    else:
        print("输入的路径无效或不是目录。")