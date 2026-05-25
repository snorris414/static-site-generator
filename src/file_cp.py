import shutil
import os


def file_cp(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)

    dir_contents = os.listdir(src)
    for file in dir_contents:
        source_file = os.path.join(src, file)
        dest_file = os.path.join(dest, file)
        if not os.path.isfile(source_file):
            os.mkdir(dest_file)
            file_cp(source_file, dest_file)
        else:
            shutil.copy(source_file, dest_file)
