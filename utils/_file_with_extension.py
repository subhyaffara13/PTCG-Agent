import os

def _file_with_extension(directory: StrPath, extension: str | tuple[str, ...]):
    matching = (f for f in os.listdir(directory) if f.endswith(extension))
    try:
        (file,) = matching
    except ValueError:
        raise ValueError(
            'No distribution was found. Ensure that `setup.py` '
            'is not empty and that it calls `setup()`.'
        ) from None
    return file

