
def _resolve_copy_target_path(
    src_file_path: str,
    src_root_path: str | None,
    is_single_file: bool,
    destination_path: str,
    destination_is_directory: bool,
    destination_exists_as_directory: bool,
    merge_contents: bool,
) -> str:
    basename = src_file_path.rsplit("/", 1)[-1]
    if is_single_file:
        if destination_path == "":
            return basename
        if destination_is_directory:
            return f"{destination_path.rstrip('/')}/{basename}"
        return destination_path

    if src_root_path is None:
        rel_path = src_file_path
    elif src_file_path.startswith(src_root_path + "/"):
        rel_path = src_file_path[len(src_root_path) + 1 :]
    elif src_file_path == src_root_path:
        rel_path = src_file_path.rsplit("/", 1)[-1]
    else:
        raise ValueError(f"Unexpected source path while copying folder: '{src_file_path}'.")

    if rel_path == "":
        raise ValueError("Cannot copy an empty relative path.")

    # Rsync-style trailing slash on source means "copy contents of" — skip nesting.
    # Without trailing slash, match `cp -r` behavior: nest source folder inside
    # existing destination directory. Non-existing destination always uses rename semantics.
    if destination_exists_as_directory and src_root_path is not None and not merge_contents:
        src_dir_basename = src_root_path.rsplit("/", 1)[-1]
        rel_path = f"{src_dir_basename}/{rel_path}"

    if destination_path == "":
        return rel_path
    return f"{destination_path.rstrip('/')}/{rel_path}"

