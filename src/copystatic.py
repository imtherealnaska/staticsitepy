import os
import shutil


def copy_files_recursive(src, dest):
    if not os.path.exists(dest):
        os.mkdir(dest)

    for file in os.listdir(src):
        from_path = os.path.join(src, file)
        dest_path = os.path.join(dest, file)
        print(f"* {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path , dest_path)
        else:
            copy_files_recursive(from_path , dest_path)
