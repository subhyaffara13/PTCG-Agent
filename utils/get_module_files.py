
def get_module_files(
    src_directory: str, blacklist: Sequence[str], list_all: bool = False
) -> list[str]:
    """Given a package directory return a list of all available python
    module's files in the package and its subpackages.

    :param src_directory:
      path of the directory corresponding to the package

    :param blacklist: iterable
      list of files or directories to ignore.

    :param list_all:
        get files from all paths, including ones without __init__.py

    :return:
      the list of all available python module's files in the package and
      its subpackages
    """
    files: list[str] = []
    for directory, dirnames, filenames in os.walk(src_directory):
        if directory in blacklist:
            continue
        _handle_blacklist(blacklist, dirnames, filenames)
        # check for __init__.py
        if not list_all and {"__init__.py", "__init__.pyi"}.isdisjoint(filenames):
            dirnames[:] = ()
            continue
        for filename in filenames:
            if _is_python_file(filename):
                src = os.path.join(directory, filename)
                files.append(src)
    return files

