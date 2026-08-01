
def is_mambapy_available() -> bool:
    return is_torch_available() and _is_package_available("mambapy")[0]

