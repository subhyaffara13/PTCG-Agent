
def register_mime(id: str, mimetype: str) -> None:
    """
    Registers an image MIME type by populating ``Image.MIME``. This function
    should not be used in application code.

    ``Image.MIME`` provides a mapping from image format identifiers to mime
    formats, but :py:meth:`~PIL.ImageFile.ImageFile.get_format_mimetype` can
    provide a different result for specific images.

    :param id: An image format identifier.
    :param mimetype: The image MIME type for this format.
    """
    MIME[id.upper()] = mimetype

