
def _set_hipcc_runtime_lib(is_standalone, debug) -> None:
    if is_standalone:
        if debug:
            COMMON_HIP_FLAGS.append('-fms-runtime-lib=static_dbg')
        else:
            COMMON_HIP_FLAGS.append('-fms-runtime-lib=static')
    else:
        if debug:
            COMMON_HIP_FLAGS.append('-fms-runtime-lib=dll_dbg')
        else:
            COMMON_HIP_FLAGS.append('-fms-runtime-lib=dll')

