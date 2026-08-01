
def _python_requires(dist: Distribution, val: str, _root_dir: StrPath | None):
    _set_config(dist, "python_requires", _static.SpecifierSet(val))

