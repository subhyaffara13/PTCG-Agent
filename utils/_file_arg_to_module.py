import os

def _file_arg_to_module(filename: str) -> str:
    filename, _ = os.path.splitext(filename)
    parts = filename.split("/")  # not os.sep since it comes from test data
    if parts[-1] == "__init__":
        parts.pop()
    return ".".join(parts)

