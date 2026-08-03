import os

def is_package_source(source: BuildSource) -> bool:
    return source.path is not None and os.path.split(source.path)[1] == "__init__.py"

