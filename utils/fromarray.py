
def fromarray(obj: SupportsArrayInterface, mode: str | None = None) -> Image:
    """
    Creates an image memory from an object exporting the array interface
    (using the buffer protocol)::

      from PIL import Image
      import numpy as np
      a = np.zeros((5, 5))
      im = Image.fromarray(a)

    If ``obj`` is not contiguous, then the ``tobytes`` method is called
    and :py:func:`~PIL.Image.frombuffer` is used.

    In the case of NumPy, be aware that Pillow modes do not always correspond
    to NumPy dtypes. Pillow modes only offer 1-bit pixels, 8-bit pixels,
    32-bit signed integer pixels, and 32-bit floating point pixels.

    Pillow images can also be converted to arrays::

      from PIL import Image
      import numpy as np
      im = Image.open("hopper.jpg")
      a = np.asarray(im)

    When converting Pillow images to arrays however, only pixel values are
    transferred. This means that P and PA mode images will lose their palette.

    :param obj: Object with array interface
    :param mode: Optional mode to use when reading ``obj``. Since pixel values do not
      contain information about palettes or color spaces, this can be used to place
      grayscale L mode data within a P mode image, or read RGB data as YCbCr for
      example.

      See: :ref:`concept-modes` for general information about modes.
    :returns: An image object.

    .. versionadded:: 1.1.6
    """
    arr = obj.__array_interface__
    shape = arr["shape"]
    ndim = len(shape)
    strides = arr.get("strides", None)
    try:
        typekey = (1, 1) + shape[2:], arr["typestr"]
    except KeyError as e:
        if mode is not None:
            typekey = None
            color_modes: list[str] = []
        else:
            msg = "Cannot handle this data type"
            raise TypeError(msg) from e
    if typekey is not None:
        try:
            typemode, rawmode, color_modes = _fromarray_typemap[typekey]
        except KeyError as e:
            typekey_shape, typestr = typekey
            msg = f"Cannot handle this data type: {typekey_shape}, {typestr}"
            raise TypeError(msg) from e
    if mode is not None:
        if mode != typemode and mode not in color_modes:
            deprecate("'mode' parameter for changing data types", 13)
        rawmode = mode
    else:
        mode = typemode
    if mode in ["1", "L", "I", "P", "F"]:
        ndmax = 2
    elif mode == "RGB":
        ndmax = 3
    else:
        ndmax = 4
    if ndim > ndmax:
        msg = f"Too many dimensions: {ndim} > {ndmax}."
        raise ValueError(msg)

    size = 1 if ndim == 1 else shape[1], shape[0]
    if strides is not None:
        if hasattr(obj, "tobytes"):
            obj = obj.tobytes()
        elif hasattr(obj, "tostring"):
            obj = obj.tostring()
        else:
            msg = "'strides' requires either tobytes() or tostring()"
            raise ValueError(msg)

    return frombuffer(mode, size, obj, "raw", rawmode, 0, 1)

