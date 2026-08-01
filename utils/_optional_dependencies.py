
def _optional_dependencies(dist: Distribution, val: dict, _root_dir: StrPath | None):
    if getattr(dist, "extras_require", None):
        msg = "`extras_require` overwritten in `pyproject.toml` (optional-dependencies)"
        SetuptoolsWarning.emit(msg)
    dist.extras_require = val

