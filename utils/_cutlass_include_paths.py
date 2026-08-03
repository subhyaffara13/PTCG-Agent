import os

def _cutlass_include_paths() -> list[str]:
    cutlass_path = _cutlass_path()
    return [
        # Use realpath to get canonical absolute paths, in order not to mess up cache keys
        os.path.realpath(os.path.join(cutlass_path, path))
        for path in _cutlass_paths()
    ]

