import os

def find_module_path_using_sys_path(module: str, sys_path: list[str]) -> str | None:
    relative_candidates = (
        module.replace(".", "/") + ".py",
        os.path.join(module.replace(".", "/"), "__init__.py"),
    )
    for base in sys_path:
        for relative_path in relative_candidates:
            path = os.path.join(base, relative_path)
            if os.path.isfile(path):
                return path
    return None

