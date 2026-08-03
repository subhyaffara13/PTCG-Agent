import os

def get_ckpt_prefix_path(ckpt_dir):
    # get prefix
    sub_folder_dir = None
    for o in os.listdir(ckpt_dir):
        sub_folder_dir = os.path.join(ckpt_dir, o)
        break
    if os.path.isfile(sub_folder_dir):
        sub_folder_dir = ckpt_dir
    unique_file_name = str(glob.glob(sub_folder_dir + "/*data-00000-of-00001"))
    prefix = (unique_file_name.rpartition(".")[0]).split("/")[-1]

    return os.path.join(sub_folder_dir, prefix)

