
def _use_fb_internal_macros() -> list[str]:
    if not _IS_WINDOWS:
        if config.is_fbcode():
            fb_internal_macros = [
                "C10_USE_GLOG",
                "C10_USE_MINIMAL_GLOG",
                "C10_DISABLE_TENSORIMPL_EXTENSIBILITY",
            ]
            if platform.machine() == "x86_64":
                fb_internal_macros += [
                    "ATEN_MKL_ENABLED_FBCODE=1",
                    "ATEN_MKLDNN_ENABLED_FBCODE=1",
                ]
            return fb_internal_macros
        else:
            return []
    else:
        return []

