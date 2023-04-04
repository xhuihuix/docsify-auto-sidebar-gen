import os
import shutil

# 定义要处理的根目录路径
base_dir = 'D:\MyData\Data\Docsify\docs'


def check_file_extension(file_path, extension):
    """
    检查文件后缀是否为指定的后缀
    :param file_path: 文件路径
    :param extension: 指定的后缀，例如".txt"
    :return: 如果文件后缀为指定的后缀，返回True；否则返回False
    """
    file_extension = os.path.splitext(file_path)[1] # 获取文件后缀
    if file_extension == extension:
        return True
    else:
        return False



def save_structure(root_dir, base_dir=base_dir):
    """
    遍历指定目录及其所有子目录，生成并保存目录结构。
    :param root_dir: 要处理的根目录路径
    """
    # 遍历根目录下的所有文件和子目录
    for root, dirs, files in os.walk(root_dir):
        # 构建当前目录的结构字符串
        subdir_structure = ''
        subdir_name = os.path.basename(root) # 获取当前目录的名字
        subdir_structure += os.path.relpath(root, base_dir) + '\n'
        for file in files:
            # 将当前目录下的所有文件添加到目录结构字符串中
            subdir_structure += "  - ["+ file + "](" + os.path.join(subdir_name, file) + ')\n'
        # 如果当前目录中有子目录，则递归遍历所有子目录
        for subdir in dirs:
            subdir_path = os.path.join(root, subdir)
            subdir_structure += "  " + save_structure(subdir_path, base_dir).replace("\n","\n  ") # 递归调用
        # 将目录结构字符串写入名为struct.txt的文件中
        with open(os.path.join(root, 'struct.txt'), 'w') as f:
            f.write(subdir_structure)
        # 返回当前目录的结构字符串
        return subdir_structure

save_structure(base_dir, base_dir)