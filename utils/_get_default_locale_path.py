import pathlib

def _get_default_locale_path() -> pathlib.Path | None:
    package = __spec__ and __spec__.parent
    if not package:
        return None

    import importlib.resources

    with importlib.resources.as_file(importlib.resources.files(package)) as pkg:
        return pkg / "locale"

