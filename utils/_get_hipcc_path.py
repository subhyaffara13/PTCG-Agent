
def _get_hipcc_path():
    if IS_WINDOWS:
        # mypy thinks ROCM_VERSION is None but it will never be None here
        hipcc_exe = 'hipcc.exe' if ROCM_VERSION >= (6, 4) else 'hipcc.bat'  # type: ignore[operator]
        return _join_rocm_home('bin', hipcc_exe)
    else:
        return _join_rocm_home('bin', 'hipcc')

