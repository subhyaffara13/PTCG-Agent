import pathlib

def find_test_files(pattern: str, exclude: list[str] | None = None) -> list[str]:
    return [
        path.name
        for path in (pathlib.Path(test_data_prefix).rglob(pattern))
        if path.name not in (exclude or [])
    ]

