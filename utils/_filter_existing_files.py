import os

def _filter_existing_files(filepaths: Iterable[StrPath]) -> Iterator[StrPath]:
    for path in filepaths:
        if os.path.isfile(path):
            yield path
        else:
            SetuptoolsWarning.emit(f"File {path!r} cannot be found")

