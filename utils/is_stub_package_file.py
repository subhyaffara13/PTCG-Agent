import os

def is_stub_package_file(file: str) -> bool:
    # Use hacky heuristics to check whether file is part of a PEP 561 stub package.
    if not file.endswith(".pyi"):
        return False
    return any(component.endswith("-stubs") for component in os.path.split(os.path.abspath(file)))

