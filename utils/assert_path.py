from pathlib import Path


def assert_path(pkg, expected):
    # __path__ is not guaranteed to exist, so we have to account for that
    if pkg.__path__:
        path = next(iter(pkg.__path__), None)
        if path:
            assert str(Path(path).resolve()) == expected

