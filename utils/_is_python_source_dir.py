
def _is_python_source_dir(d):
    """
    Return True if the target directory appears to point to an
    un-installed Python.
    """
    modules = pathlib.Path(d).joinpath('Modules')
    return any(modules.joinpath(fn).is_file() for fn in ('Setup', 'Setup.local'))

