
def set_filename(filename: str, insert_device_ordinal: bool = False) -> None:
    r"""Set the filename to use for input/output of tuning results.

    If :attr:`insert_device_ordinal` is ``True`` then the current device ordinal
    will be added to the given filename automatically. This can be used in a
    1-process-per-gpu scenario to ensure all processes write to a separate file.
    """
    torch._C._cuda_tunableop_set_filename(filename, insert_device_ordinal)  # type: ignore[attr-defined]

