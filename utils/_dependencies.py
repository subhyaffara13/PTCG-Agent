
def _dependencies(dist: Distribution, val: list, _root_dir: StrPath | None):
    if getattr(dist, "install_requires", []):
        msg = "`install_requires` overwritten in `pyproject.toml` (dependencies)"
        SetuptoolsWarning.emit(msg)
    dist.install_requires = val

