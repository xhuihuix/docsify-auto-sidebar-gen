import os
import shutil

# 定义要处理的根目录路径
base_dir = 'D:\MyData\Data\Docsify\docs'
start_with = ['_', '.']
show_file = ['.md']
ignore_file_name = ['README', "Test"]

def check_file_extension(file_path):
    """
    检查文件后缀是否为指定的后缀
    :param file_path: 文件路径
    :return: 如果文件后缀为指定的后缀，返回True；否则返回False
    """
    file_extension = os.path.splitext(file_path)[1] # 获取文件后缀
    if file_extension in show_file:
        return True
    else:
        return False

def check_file_name_satified(file_path):
    """
    获取文件名（不包括扩展名）
    :param file_path: 文件路径
    :return: 文件名（不包括扩展名）
    """
    file_name_with_extension = os.path.basename(file_path)
    file_name = os.path.splitext(file_name_with_extension)[0]
    if file_name[0] in start_with or file_name in ignore_file_name:
        return False
    return True

def save_structure(root_dir, base_dir=base_dir, depth=0):
    """
    遍历指定目录及其所有子目录，生成并保存目录结构。
    :param root_dir: 要处理的根目录路径
    :param base_dir: 用来获得root_dir对base_dir的相对路径
    :param depth: 递归深度，文件夹深度
    """
    # 遍历根目录下的所有文件和子目录
    for root, dirs, files in os.walk(root_dir):
        # 构建当前目录的结构字符串
        subdir_structure = ''
        subdir_name = os.path.basename(root) # 获取当前目录的名字


        if depth != 0:
            subdir_structure += "- [" + subdir_name + "](" + os.path.relpath(root, base_dir) + '\)\n'  # 当前路径，第一行文字
        else:
            subdir_structure += "- [" + "首页" + "](" + os.path.relpath(root, base_dir) + '\)\n'  # 当前路径，第一行文字


        for file in files:
            # 将当前目录下的所有文件添加到目录结构字符串中
            if check_file_name_satified(os.path.join(root, file)):
                if check_file_extension(file):
                    subdir_structure += "  " + "- ["+ file + "](" + os.path.relpath(os.path.join(root, file), base_dir) + ')\n'  # 该目录下所有文件信息，格式：[文件名](文件相对路径)


        # 如果当前目录中有子目录，则递归遍历所有子目录
        for subdir in dirs:
            subdir_path = os.path.join(root, subdir)
            if check_file_name_satified(subdir_path):
                next_struct = save_structure(subdir_path, base_dir, depth+1)
                next_struct = next_struct[:-1] if next_struct.endswith("\n") else next_struct
                next_struct = next_struct.replace("\n","\n  ") + "\n"
                subdir_structure += "  " + next_struct  # 递归调用,构造md语法

        back_struct = subdir_structure
        if depth == 1:
            subdir_structure = "- [" + "返回首页" + "](" + "" + '\?id=main)\n' + subdir_structure  # 当前路径，第一行文字
        elif depth != 0:
            abs_pre_path = os.path.abspath(os.path.join(root, ".."))
            rel_pre_path = os.path.relpath(abs_pre_path, base_dir)
            subdir_structure = "- [" + "返回上一级" + "](" + rel_pre_path + '\)\n' + subdir_structure  # 当前路径，第一行文字

        # if depth == 1:
        #     subdir_structure = "- [" + "返回首页" + "](" + "" + '\?id=main)\n' + subdir_structure  # 当前路径，第一行文字

        # 将目录结构字符串写入名为REAMD.md _sidebar.md的文件中
        subdir_structure = subdir_structure.replace('\\','/')
        with open(os.path.join(root, 'README.md'), 'w', encoding="utf-8") as f:
            f.write(subdir_structure)
        with open(os.path.join(root, '_sidebar.md'), 'w', encoding="utf-8") as f:
            f.write(subdir_structure)
        # 返回当前目录的结构字符串


        return back_struct

save_structure(base_dir, base_dir, 0)