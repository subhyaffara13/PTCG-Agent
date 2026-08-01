
def copy_structure(
    src_fs: FS,
    dst_fs: FS,
    src_root: str = "/",
    dst_root: str = "/",
):
    if src_fs is dst_fs and isbase(src_root, dst_root):
        raise IllegalDestination(f"cannot copy {src_fs!r} to itself")

    dst_fs.makedirs(dst_root, recreate=True)
    for dir_path in src_fs.walk.dirs(src_root):
        dst_fs.makedir(combine(dst_root, frombase(src_root, dir_path)), recreate=True)

