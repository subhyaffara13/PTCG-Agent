
def _cutlass_path() -> str:
    if config.is_fbcode():
        from libfb.py import parutil

        return parutil.get_dir_path("cutlass-4-headers")
    else:
        return config.cutlass.cutlass_dir

