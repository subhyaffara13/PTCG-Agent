
def split_aot_inductor_output_path(path: str) -> tuple[str, str]:
    def get_module_ext_type() -> str:
        if _IS_WINDOWS:
            return ".pyd"
        else:
            return ".so"

    """Returns the path where the AOT Inductor compiled kernels are stored."""
    if path.endswith(get_module_ext_type()):
        return os.path.split(path)
    elif path.endswith(".pt2"):
        return os.path.split(path)
    else:
        return path, ""

