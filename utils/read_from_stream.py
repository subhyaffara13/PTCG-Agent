import os

def readFromStream(substrate, size=-1, context=None):
    """Read from the stream.

    Parameters
    ----------
    substrate: :py:class:`IOBase`
        Stream to read from.

    Keyword parameters
    ------------------
    size: :py:class:`int`
        How many bytes to read (-1 = all available)

    context: :py:class:`dict`
        Opaque caller context will be attached to exception objects created
        by this function.

    Yields
    ------
    : :py:class:`bytes` or :py:class:`str` or :py:class:`SubstrateUnderrunError`
        Read data or :py:class:`~pyasn1.error.SubstrateUnderrunError`
        object if no `size` bytes is readily available in the stream. The
        data type depends on Python major version

    Raises
    ------
    : :py:class:`~pyasn1.error.EndOfStreamError`
        Input stream is exhausted
    """
    while True:
        # this will block unless stream is non-blocking
        received = substrate.read(size)
        if received is None:  # non-blocking stream can do this
            yield error.SubstrateUnderrunError(context=context)

        elif not received and size != 0:  # end-of-stream
            raise error.EndOfStreamError(context=context)

        elif len(received) < size:
            substrate.seek(-len(received), os.SEEK_CUR)

            # behave like a non-blocking stream
            yield error.SubstrateUnderrunError(context=context)

        else:
            break

    yield received

