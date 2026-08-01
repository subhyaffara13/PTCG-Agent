
def _get_build_root() -> str:
    global _BUILD_ROOT
    if _BUILD_ROOT is None:
        _BUILD_ROOT = _make_temp_dir(prefix="benchmark_utils_jit_build")
        # pyrefly: ignore [missing-argument]
        atexit.register(shutil.rmtree, _BUILD_ROOT)
    return _BUILD_ROOT

