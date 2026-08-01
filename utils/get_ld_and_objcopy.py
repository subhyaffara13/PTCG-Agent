
def get_ld_and_objcopy(use_relative_path: bool) -> tuple[str, str]:
    if _IS_WINDOWS:
        raise RuntimeError("Windows is not supported yet.")
    else:
        if config.is_fbcode():
            ld = build_paths.ld
            objcopy = (
                build_paths.objcopy_fallback
                if use_relative_path
                else build_paths.objcopy
            )
        else:
            ld = "ld"
            objcopy = "objcopy"
    return ld, objcopy

