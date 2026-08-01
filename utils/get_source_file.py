
def get_source_file(
    filename: str, include_no_ext: bool = False, prefer_stubs: bool = False
) -> str:
    """Given a python module's file name return the matching source file
    name (the filename will be returned identically if it's already an
    absolute path to a python source file).

    :param filename: python module's file name

    :raise NoSourceFile: if no source file exists on the file system

    :return: the absolute path of the source file if it exists
    """
    filename = os.path.abspath(_path_from_filename(filename))
    base, orig_ext = os.path.splitext(filename)
    orig_ext = orig_ext.lstrip(".")
    if orig_ext not in PY_SOURCE_EXTS and os.path.exists(f"{base}.{orig_ext}"):
        return f"{base}.{orig_ext}"
    for ext in PY_SOURCE_EXTS_STUBS_FIRST if prefer_stubs else PY_SOURCE_EXTS:
        source_path = f"{base}.{ext}"
        if os.path.exists(source_path):
            return source_path
    if include_no_ext and not orig_ext and os.path.exists(base):
        return base
    raise NoSourceFile(filename)

