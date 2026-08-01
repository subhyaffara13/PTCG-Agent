
def frombytes(
    mode: str,
    size: tuple[int, int],
    data: DecoderInput,
    decoder_name: str = "raw",
    *args: Any,
) -> Image:
    """
    Creates a copy of an image memory from pixel data in a buffer.

    In its simplest form, this function takes three arguments
    (mode, size, and unpacked pixel data).

    You can also use any pixel decoder supported by PIL. For more
    information on available decoders, see the section
    :ref:`Writing Your Own File Codec <file-codecs>`.

    Note that this function decodes pixel data only, not entire images.
    If you have an entire image in a string, wrap it in a
    :py:class:`~io.BytesIO` object, and use :py:func:`~PIL.Image.open` to load
    it.

    :param mode: The image mode. See: :ref:`concept-modes`.
    :param size: The image size.
    :param data: A byte buffer containing raw data for the given mode.
    :param decoder_name: What decoder to use.
    :param args: Additional parameters for the given decoder.
    :returns: An :py:class:`~PIL.Image.Image` object.
    """

    _check_size(size)

    im = new(mode, size)
    if im.width != 0 and im.height != 0:
        decoder_args: Any = args
        if len(decoder_args) == 1 and isinstance(decoder_args[0], tuple):
            # may pass tuple instead of argument list
            decoder_args = decoder_args[0]

        if decoder_name == "raw" and decoder_args == ():
            decoder_args = mode

        im.frombytes(data, decoder_name, decoder_args)
    return im

