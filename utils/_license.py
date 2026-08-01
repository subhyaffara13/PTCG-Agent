
def _license(dist: Distribution, val: str | dict, root_dir: StrPath | None):
    from setuptools.config import expand

    if isinstance(val, str):
        if getattr(dist.metadata, "license", None):
            SetuptoolsWarning.emit("`license` overwritten by `pyproject.toml`")
            dist.metadata.license = None
        _set_config(dist, "license_expression", _static.Str(val))
    else:
        pypa_guides = "guides/writing-pyproject-toml/#license"
        SetuptoolsDeprecationWarning.emit(
            "`project.license` as a TOML table is deprecated",
            "Please use a simple string containing a SPDX expression for "
            "`project.license`. You can also use `project.license-files`. "
            "(Both options available on setuptools>=77.0.0).",
            see_url=f"https://packaging.python.org/en/latest/{pypa_guides}",
            due_date=(2027, 2, 18),  # Introduced on 2025-02-18
        )
        if "file" in val:
            # XXX: Is it completely safe to assume static?
            value = expand.read_files([val["file"]], root_dir)
            _set_config(dist, "license", _static.Str(value))
            dist._referenced_files.add(val["file"])
        else:
            _set_config(dist, "license", _static.Str(val["text"]))

