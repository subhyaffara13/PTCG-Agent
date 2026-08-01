
def is_special_module(path: str) -> bool:
    return os.path.basename(path) in ("abc.pyi", "typing.pyi", "builtins.pyi")

