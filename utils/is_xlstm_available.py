
def is_xlstm_available() -> bool:
    return is_torch_available() and _is_package_available("xlstm")[0]

