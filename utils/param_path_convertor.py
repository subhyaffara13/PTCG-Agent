from pathlib import Path


def param_path_convertor(value: str | None = None) -> Path | None:
    if value is not None:
        # allow returning any subclass of Path created by an annotated parser without converting
        # it back to a Path
        return value if isinstance(value, Path) else Path(value)
    return None

