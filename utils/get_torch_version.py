
def get_torch_version() -> str:
    _, torch_version = _is_package_available("torch", return_version=True)
    return torch_version


def get_torch_version() -> str:
    version = torch.__version__.split(".")
    return f"{int(version[0])}.{int(version[1])}"


def get_torch_version() -> str:
    return _get_version("torch")

