from typing import Callable

def register_save(
    id: str, driver: Callable[[Image, IO[bytes], str | bytes], None]
) -> None:
    """
    Registers an image save function.  This function should not be
    used in application code.

    :param id: An image format identifier.
    :param driver: A function to save images in this format.
    """
    SAVE[id.upper()] = driver

