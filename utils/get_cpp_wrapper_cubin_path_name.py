
def get_cpp_wrapper_cubin_path_name() -> str:
    return "cubin_path" if torch.version.hip is None else "hsaco_path"

