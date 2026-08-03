import sys

def _preload_cuda_lib(lib_folder: str, lib_name: str, required: bool = True) -> None:  # type: ignore[valid-type]
    """Preloads cuda library if it could not be found otherwise."""
    # Should only be called on Linux if default path resolution have failed
    if platform.system() != "Linux":
        raise AssertionError(f"Should only be called on Linux, got {platform.system()}")

    lib_path = None
    for path in sys.path:
        candidate_lib_paths = _get_cuda_dep_paths(path, lib_folder, lib_name)
        if candidate_lib_paths:
            lib_path = candidate_lib_paths[0]
            break
    if not lib_path and required:
        raise ValueError(f"{lib_name} not found in the system path {sys.path}")
    if lib_path:
        ctypes.CDLL(lib_path)

