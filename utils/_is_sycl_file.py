import os

def _is_sycl_file(path: str) -> bool:
    valid_ext = ['.sycl']
    return os.path.splitext(path)[1] in valid_ext

