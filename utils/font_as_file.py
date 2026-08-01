
def font_as_file(font):
    """
    Convert a TTFont object into a file-like object.

    Parameters
    ----------
    font : fontTools.ttLib.ttFont.TTFont
        A font object

    Returns
    -------
    BytesIO
        A file object with the font saved into it
    """
    fh = BytesIO()
    font.save(fh, reorderTables=False)
    return fh

