
def iter_slices(
    string: bytes, slice_length: int | None
) -> Generator[bytes, None, None]: ...


def iter_slices(
    string: str, slice_length: int | None
) -> Generator[str, None, None]: ...


def iter_slices(
    string: bytes | str, slice_length: int | None
) -> Generator[bytes | str, None, None]:
    """Iterate over slices of a string."""
    pos = 0
    if slice_length is None or slice_length <= 0:
        slice_length = len(string)
    while pos < len(string):
        yield string[pos : pos + slice_length]
        pos += slice_length


def iter_slices(string, slice_length):
    """Iterate over slices of a string."""
    pos = 0
    if slice_length is None or slice_length <= 0:
        slice_length = len(string)
    while pos < len(string):
        yield string[pos : pos + slice_length]
        pos += slice_length

