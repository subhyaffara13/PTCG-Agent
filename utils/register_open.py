
def register_open(
    id: str,
    factory: (
        Callable[[IO[bytes], str | bytes], ImageFile.ImageFile]
        | type[ImageFile.ImageFile]
    ),
    accept: Callable[[bytes], bool | str] | None = None,
) -> None:
    """
    Register an image file plugin.  This function should not be used
    in application code.

    :param id: An image format identifier.
    :param factory: An image file factory method.
    :param accept: An optional function that can be used to quickly
       reject images having another format.
    """
    id = id.upper()
    if id not in ID:
        ID.append(id)
    OPEN[id] = factory, accept

