
def copy_dir(src_fs: FS, src_path: str, dst_fs: FS, dst_path: str):
    copy_structure(src_fs, dst_fs, src_path, dst_path)

    for file_path in src_fs.walk.files(src_path):
        copy_path = combine(dst_path, frombase(src_path, file_path))
        copy_file(src_fs, file_path, dst_fs, copy_path)

