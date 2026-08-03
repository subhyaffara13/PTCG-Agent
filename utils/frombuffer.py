from typing import Any

def frombuffer(
    mode: str,
    size: tuple[int, int],
    data: bytes | SupportsArrayInterface,
    decoder_name: str = "raw",
    *args: Any,
) -> Image:
    """
    Creates an image memory referencing pixel data in a byte buffer.

    This function is similar to :py:func:`~PIL.Image.frombytes`, but uses data
    in the byte buffer, where possible.  This means that changes to the
    original buffer object are reflected in this image).  Not all modes can
    share memory; supported modes include "L", "RGBX", "RGBA", and "CMYK".

    Note that this function decodes pixel data only, not entire images.
    If you have an entire image file in a string, wrap it in a
    :py:class:`~io.BytesIO` object, and use :py:func:`~PIL.Image.open` to load it.

    The default parameters used for the "raw" decoder differs from that used for
    :py:func:`~PIL.Image.frombytes`. This is a bug, and will probably be fixed in a
    future release. The current release issues a warning if you do this; to disable
    the warning, you should provide the full set of parameters. See below for details.

    :param mode: The image mode. See: :ref:`concept-modes`.
    :param size: The image size.
    :param data: A bytes or other buffer object containing raw
        data for the given mode.
    :param decoder_name: What decoder to use.
    :param args: Additional parameters for the given decoder.  For the
        default encoder ("raw"), it's recommended that you provide the
        full set of parameters::

            frombuffer(mode, size, data, "raw", mode, 0, 1)

    :returns: An :py:class:`~PIL.Image.Image` object.

    .. versionadded:: 1.1.4
    """

    _check_size(size)

    # may pass tuple instead of argument list
    if len(args) == 1 and isinstance(args[0], tuple):
        args = args[0]

    if decoder_name == "raw":
        if args == ():
            args = mode, 0, 1
        if args[0] in _MAPMODES:
            im = new(mode, (0, 0))
            im = im._new(core.map_buffer(data, size, decoder_name, 0, args))
            if mode == "P":
                from . import ImagePalette

                im.palette = ImagePalette.ImagePalette("RGB", im.im.getpalette("RGB"))
            im.readonly = 1
            return im

    return frombytes(mode, size, data, decoder_name, args)


def frombuffer(buffer: bytes | Any, dtype: DTypeLike = float,
               count: int = -1, offset: int = 0) -> Array:
  r"""Convert a buffer into a 1-D JAX array.

  JAX implementation of :func:`numpy.frombuffer`.

  Args:
    buffer: an object containing the data. It must be either a bytes object with
      a length that is an integer multiple of the dtype element size, or
      it must be an object exporting the `Python buffer interface`_.
    dtype: optional. Desired data type for the array. Default is ``float64``.
      This specifies the dtype used to parse the buffer, but note that after parsing,
      64-bit values will be cast to 32-bit JAX arrays if the ``jax_enable_x64``
      flag is set to ``False``.
    count: optional integer specifying the number of items to read from the buffer.
      If -1 (default), all items from the buffer are read.
    offset: optional integer specifying the number of bytes to skip at the beginning
      of the buffer. Default is 0.

  Returns:
    A 1-D JAX array representing the interpreted data from the buffer.

  See also:
    - :func:`jax.numpy.fromstring`: convert a string of text into 1-D JAX array.

  Examples:
    Using a bytes buffer:

    >>> buf = b"\x00\x01\x02\x03\x04"
    >>> jnp.frombuffer(buf, dtype=jnp.uint8)
    Array([0, 1, 2, 3, 4], dtype=uint8)
    >>> jnp.frombuffer(buf, dtype=jnp.uint8, offset=1)
    Array([1, 2, 3, 4], dtype=uint8)

    Constructing a JAX array via the Python buffer interface, using Python's
    built-in :mod:`array` module.

    >>> from array import array
    >>> pybuffer = array('i', [0, 1, 2, 3, 4])
    >>> jnp.frombuffer(pybuffer, dtype=jnp.int32)
    Array([0, 1, 2, 3, 4], dtype=int32)

  .. _Python buffer interface: https://docs.python.org/3/c-api/buffer.html
  """
  return asarray(np.frombuffer(buffer=buffer, dtype=dtype, count=count, offset=offset))

