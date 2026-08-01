
def register_decoder(name: str, decoder: type[ImageFile.PyDecoder]) -> None:
    """
    Registers an image decoder.  This function should not be
    used in application code.

    :param name: The name of the decoder
    :param decoder: An ImageFile.PyDecoder object

    .. versionadded:: 4.1.0
    """
    DECODERS[name] = decoder

