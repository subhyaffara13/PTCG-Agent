
def _copy_one(
    name,
    *,
    src,
    dst,
    preserve_symlinks,
    verbose,
    preserve_mode,
    preserve_times,
    update,
):
    src_name = os.path.join(src, name)
    dst_name = os.path.join(dst, name)

    if name.startswith('.nfs'):
        # skip NFS rename files
        return

    if preserve_symlinks and os.path.islink(src_name):
        link_dest = os.readlink(src_name)
        if verbose >= 1:
            log.info("linking %s -> %s", dst_name, link_dest)
        os.symlink(link_dest, dst_name)
        yield dst_name

    elif os.path.isdir(src_name):
        yield from copy_tree(
            src_name,
            dst_name,
            preserve_mode,
            preserve_times,
            preserve_symlinks,
            update,
            verbose=verbose,
        )
    else:
        file_util.copy_file(
            src_name,
            dst_name,
            preserve_mode,
            preserve_times,
            update,
            verbose=verbose,
        )
        yield dst_name

