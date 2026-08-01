
def register_save_all(
    id: str, driver: Callable[[Image, IO[bytes], str | bytes], None]
) -> None:
    """
    Registers an image function to save all the frames
    of a multiframe format.  This function should not be
    used in application code.

    :param id: An image format identifier.
    :param driver: A function to save images in this format.
    """
    SAVE_ALL[id.upper()] = driver

