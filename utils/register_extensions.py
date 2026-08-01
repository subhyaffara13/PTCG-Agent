
def register_extensions(id: str, extensions: list[str]) -> None:
    """
    Registers image extensions.  This function should not be
    used in application code.

    :param id: An image format identifier.
    :param extensions: A list of extensions used for this format.
    """
    for extension in extensions:
        register_extension(id, extension)

