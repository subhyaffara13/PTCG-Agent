
def _spec_from_modpath(
    modpath: list[str],
    path: Sequence[str] | None = None,
    context: str | None = None,
) -> spec.ModuleSpec:
    """Given a mod path (i.e. split module / package name), return the
    corresponding spec.

    this function is used internally, see `file_from_modpath`'s
    documentation for more information
    """
    assert modpath
    location = None
    if context is not None:
        try:
            found_spec = spec.find_spec(modpath, [context])
            location = found_spec.location
        except ImportError:
            found_spec = spec.find_spec(modpath, path)
            location = found_spec.location
    else:
        found_spec = spec.find_spec(modpath, path)
    if found_spec.type == spec.ModuleType.PY_COMPILED:
        try:
            assert found_spec.location is not None
            location = get_source_file(found_spec.location)
            return found_spec._replace(
                location=location, type=spec.ModuleType.PY_SOURCE
            )
        except NoSourceFile:
            return found_spec._replace(location=location)
    elif found_spec.type == spec.ModuleType.C_BUILTIN:
        # integrated builtin module
        return found_spec._replace(location=None)
    elif found_spec.type == spec.ModuleType.PKG_DIRECTORY:
        assert found_spec.location is not None
        location = _has_init(found_spec.location)
        return found_spec._replace(location=location, type=spec.ModuleType.PY_SOURCE)
    return found_spec

