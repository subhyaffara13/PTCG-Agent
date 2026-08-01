
def fromarrow(
    obj: SupportsArrowArrayInterface, mode: str, size: tuple[int, int]
) -> Image:
    """Creates an image with zero-copy shared memory from an object exporting
    the arrow_c_array interface protocol::

      from PIL import Image
      import pyarrow as pa
      arr = pa.array([0]*(5*5*4), type=pa.uint8())
      im = Image.fromarrow(arr, 'RGBA', (5, 5))

    If the data representation of the ``obj`` is not compatible with
    Pillow internal storage, a ValueError is raised.

    Pillow images can also be converted to Arrow objects::

      from PIL import Image
      import pyarrow as pa
      im = Image.open('hopper.jpg')
      arr = pa.array(im)

    As with array support, when converting Pillow images to arrays,
    only pixel values are transferred. This means that P and PA mode
    images will lose their palette.

    :param obj: Object with an arrow_c_array interface
    :param mode: Image mode.
    :param size: Image size. This must match the storage of the arrow object.
    :returns: An Image object

    Note that according to the Arrow spec, both the producer and the
    consumer should consider the exported array to be immutable, as
    unsynchronized updates will potentially cause inconsistent data.

    See: :ref:`arrow-support` for more detailed information

    .. versionadded:: 11.2.1

    """
    if not hasattr(obj, "__arrow_c_array__"):
        msg = "arrow_c_array interface not found"
        raise ValueError(msg)

    schema_capsule, array_capsule = obj.__arrow_c_array__()
    _im = core.new_arrow(mode, size, schema_capsule, array_capsule)
    if _im:
        return Image()._new(_im)

    msg = "new_arrow returned None without an exception"
    raise ValueError(msg)

