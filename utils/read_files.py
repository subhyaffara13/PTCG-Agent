import os

def read_files(
    filepaths: StrPath | Iterable[StrPath], root_dir: StrPath | None = None
) -> str:
    """Return the content of the files concatenated using ``\n`` as str

    This function is sandboxed and won't reach anything outside ``root_dir``

    (By default ``root_dir`` is the current directory).
    """
    from more_itertools import always_iterable

    root_dir = os.path.abspath(root_dir or os.getcwd())
    _filepaths = (os.path.join(root_dir, path) for path in always_iterable(filepaths))
    return '\n'.join(
        _read_file(path)
        for path in _filter_existing_files(_filepaths)
        if _assert_local(path, root_dir)
    )

