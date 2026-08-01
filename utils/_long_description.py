
def _long_description(
    dist: Distribution, val: _ProjectReadmeValue, root_dir: StrPath | None
):
    from setuptools.config import expand

    file: str | tuple[()]
    if isinstance(val, str):
        file = val
        text = expand.read_files(file, root_dir)
        ctype = _guess_content_type(file)
    else:
        file = val.get("file") or ()
        text = val.get("text") or expand.read_files(file, root_dir)
        ctype = val["content-type"]

    # XXX: Is it completely safe to assume static?
    _set_config(dist, "long_description", _static.Str(text))

    if ctype:
        _set_config(dist, "long_description_content_type", _static.Str(ctype))

    if file:
        dist._referenced_files.add(file)

