
def select_backend(xp: ModuleType, cython_compatible: bool):
    """Select the backend for the given array library.

    We need this selection function because the Cython backend for numpy does not
    support quaternions of arbitrary dimensions. We therefore only use the Array API
    backend for numpy if we are dealing with rotations of more than one leading
    dimension.
    """
    if is_numpy(xp) and not cython_compatible:
        return xp_backend
    return backend_registry.get(xp, xp_backend)


def select_backend(xp: ModuleType, cython_compatible: bool):
    """Select the backend for the given array library.

    We need this selection function because the Cython backend for numpy does not
    support quaternions of arbitrary dimensions. We therefore only use the Array API
    backend for numpy if we are dealing with rotations of more than one leading
    dimension.
    """
    if is_numpy(xp) and not cython_compatible:
        return xp_backend
    return backend_registry.get(xp, xp_backend)


def select_backend() -> Backend:
    if _should_use_importlib_metadata():
        from . import importlib

        return cast(Backend, importlib)

    _emit_pkg_resources_deprecation_if_needed()

    from . import pkg_resources

    return cast(Backend, pkg_resources)

