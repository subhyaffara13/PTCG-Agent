
def copy_fs(src_fs: FS, dst_fs: FS):
    copy_dir(src_fs, "/", dst_fs, "/")

