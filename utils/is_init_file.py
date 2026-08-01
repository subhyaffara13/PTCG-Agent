
def is_init_file(path: str) -> bool:
    return os.path.basename(path) in ("__init__.py", "__init__.pyi")

