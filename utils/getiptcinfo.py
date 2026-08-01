
def getiptcinfo(
    im: ImageFile.ImageFile,
) -> dict[tuple[int, int], bytes | list[bytes]] | None:
    """
    Get IPTC information from TIFF, JPEG, or IPTC file.

    :param im: An image containing IPTC data.
    :returns: A dictionary containing IPTC information, or None if
        no IPTC information block was found.
    """
    from . import JpegImagePlugin, TiffImagePlugin

    data = None

    if isinstance(im, IptcImageFile):
        # return info dictionary right away
        return {k: v for k, v in im.info.items() if isinstance(k, tuple)}

    elif isinstance(im, JpegImagePlugin.JpegImageFile):
        # extract the IPTC/NAA resource
        photoshop = im.info.get("photoshop")
        if photoshop:
            data = photoshop.get(0x0404)

    elif isinstance(im, TiffImagePlugin.TiffImageFile):
        # get raw data from the IPTC/NAA tag (PhotoShop tags the data
        # as 4-byte integers, so we cannot use the get method...)
        try:
            data = im.tag_v2._tagdata[TiffImagePlugin.IPTC_NAA_CHUNK]
        except KeyError:
            pass

    if data is None:
        return None  # no properties

    # create an IptcImagePlugin object without initializing it
    class FakeImage:
        pass

    fake_im = FakeImage()
    fake_im.__class__ = IptcImageFile  # type: ignore[assignment]
    iptc_im = cast(IptcImageFile, fake_im)

    # parse the IPTC information chunk
    iptc_im.info = {}
    iptc_im.fp = BytesIO(data)

    try:
        iptc_im._open()
    except (IndexError, KeyError):
        pass  # expected failure

    return {k: v for k, v in iptc_im.info.items() if isinstance(k, tuple)}

