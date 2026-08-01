
def _path_from_filename(filename: str, is_jython: bool = IS_JYTHON) -> str:
    if not is_jython:
        return filename
    head, has_pyclass, _ = filename.partition("$py.class")
    if has_pyclass:
        return head + ".py"
    return filename

