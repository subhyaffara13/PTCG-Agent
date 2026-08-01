
def from_array(a, mode=None, info={}):
    """Create a PNG :class:`Image` object from a 2- or 3-dimensional array.
    One application of this function is easy PIL-style saving:
    ``png.from_array(pixels, 'L').save('foo.png')``.

    .. note :

      The use of the term *3-dimensional* is for marketing purposes
      only.  It doesn't actually work.  Please bear with us.  Meanwhile
      enjoy the complimentary snacks (on request) and please use a
      2-dimensional array.

    Unless they are specified using the *info* parameter, the PNG's
    height and width are taken from the array size.  For a 3 dimensional
    array the first axis is the height; the second axis is the width;
    and the third axis is the channel number.  Thus an RGB image that is
    16 pixels high and 8 wide will use an array that is 16x8x3.  For 2
    dimensional arrays the first axis is the height, but the second axis
    is ``width*channels``, so an RGB image that is 16 pixels high and 8
    wide will use a 2-dimensional array that is 16x24 (each row will be
    8*3==24 sample values).

    *mode* is a string that specifies the image colour format in a
    PIL-style mode.  It can be:

    ``'L'``
      greyscale (1 channel)
    ``'LA'``
      greyscale with alpha (2 channel)
    ``'RGB'``
      colour image (3 channel)
    ``'RGBA'``
      colour image with alpha (4 channel)

    The mode string can also specify the bit depth (overriding how this
    function normally derives the bit depth, see below).  Appending
    ``';16'`` to the mode will cause the PNG to be 16 bits per channel;
    any decimal from 1 to 16 can be used to specify the bit depth.

    When a 2-dimensional array is used *mode* determines how many
    channels the image has, and so allows the width to be derived from
    the second array dimension.

    The array is expected to be a ``numpy`` array, but it can be any
    suitable Python sequence.  For example, a list of lists can be used:
    ``png.from_array([[0, 255, 0], [255, 0, 255]], 'L')``.  The exact
    rules are: ``len(a)`` gives the first dimension, height;
    ``len(a[0])`` gives the second dimension; ``len(a[0][0])`` gives the
    third dimension, unless an exception is raised in which case a
    2-dimensional array is assumed.  It's slightly more complicated than
    that because an iterator of rows can be used, and it all still
    works.  Using an iterator allows data to be streamed efficiently.

    The bit depth of the PNG is normally taken from the array element's
    datatype (but if *mode* specifies a bitdepth then that is used
    instead).  The array element's datatype is determined in a way which
    is supposed to work both for ``numpy`` arrays and for Python
    ``array.array`` objects.  A 1 byte datatype will give a bit depth of
    8, a 2 byte datatype will give a bit depth of 16.  If the datatype
    does not have an implicit size, for example it is a plain Python
    list of lists, as above, then a default of 8 is used.

    The *info* parameter is a dictionary that can be used to specify
    metadata (in the same style as the arguments to the
    :class:``png.Writer`` class).  For this function the keys that are
    useful are:

    height
      overrides the height derived from the array dimensions and allows
      *a* to be an iterable.
    width
      overrides the width derived from the array dimensions.
    bitdepth
      overrides the bit depth derived from the element datatype (but
      must match *mode* if that also specifies a bit depth).

    Generally anything specified in the
    *info* dictionary will override any implicit choices that this
    function would otherwise make, but must match any explicit ones.
    For example, if the *info* dictionary has a ``greyscale`` key then
    this must be true when mode is ``'L'`` or ``'LA'`` and false when
    mode is ``'RGB'`` or ``'RGBA'``.
    """

    # We abuse the *info* parameter by modifying it.  Take a copy here.
    # (Also typechecks *info* to some extent).
    info = dict(info)

    # Syntax check mode string.
    bitdepth = None
    try:
        mode = mode.split(";")
        if len(mode) not in (1, 2):
            raise Error()
        if mode[0] not in ("L", "LA", "RGB", "RGBA"):
            raise Error()
        if len(mode) == 2:
            try:
                bitdepth = int(mode[1])
            except:
                raise Error()
    except Error:
        raise Error("mode string should be 'RGB' or 'L;16' or similar.")
    mode = mode[0]

    # Get bitdepth from *mode* if possible.
    if bitdepth:
        if info.get("bitdepth") and bitdepth != info["bitdepth"]:
            raise Error(
                "mode bitdepth (%d) should match info bitdepth (%d)."
                % (bitdepth, info["bitdepth"])
            )
        info["bitdepth"] = bitdepth

    # Fill in and/or check entries in *info*.
    # Dimensions.
    if "size" in info:
        # Check width, height, size all match where used.
        for dimension, axis in [("width", 0), ("height", 1)]:
            if dimension in info:
                if info[dimension] != info["size"][axis]:
                    raise Error(
                        f"info[{dimension!r}] should match info['size'][{axis!r}]."
                    )
        info["width"], info["height"] = info["size"]
    if "height" not in info:
        try:
            l = len(a)
        except:
            raise Error("len(a) does not work, supply info['height'] instead.")
        info["height"] = l
    # Colour format.
    if "greyscale" in info:
        if bool(info["greyscale"]) != ("L" in mode):
            raise Error("info['greyscale'] should match mode.")
    info["greyscale"] = "L" in mode
    if "alpha" in info:
        if bool(info["alpha"]) != ("A" in mode):
            raise Error("info['alpha'] should match mode.")
    info["alpha"] = "A" in mode

    planes = len(mode)
    if "planes" in info:
        if info["planes"] != planes:
            raise Error("info['planes'] should match mode.")

    # In order to work out whether we the array is 2D or 3D we need its
    # first row, which requires that we take a copy of its iterator.
    # We may also need the first row to derive width and bitdepth.
    a, t = itertools.tee(a)
    row = next(t)
    del t
    try:
        row[0][0]
        threed = True
        testelement = row[0]
    except:
        threed = False
        testelement = row
    if "width" not in info:
        if threed:
            width = len(row)
        else:
            width = len(row) // planes
        info["width"] = width

    # Not implemented yet
    assert not threed

    if "bitdepth" not in info:
        try:
            dtype = testelement.dtype
            # goto the "else:" clause.  Sorry.
        except:
            try:
                # Try a Python array.array.
                bitdepth = 8 * testelement.itemsize
            except:
                # We can't determine it from the array element's
                # datatype, use a default of 8.
                bitdepth = 8
        else:
            # If we got here without exception, we now assume that
            # the array is a numpy array.
            if dtype.kind == "b":
                bitdepth = 1
            else:
                bitdepth = 8 * dtype.itemsize
        info["bitdepth"] = bitdepth

    for thing in "width height bitdepth greyscale alpha".split():
        assert thing in info
    return Image(a, info)

