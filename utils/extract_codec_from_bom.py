
def extract_codec_from_bom(first_line: bytes) -> str:
    """Try to extract the codec (unicode only) by checking for the BOM.

    For details about BOM see https://unicode.org/faq/utf_bom.html#BOM

    Args:
        first_line: the first line of a file

    Returns:
        a codec name

    Raises:
        ValueError: if no codec was found
    """
    for bom, codec in BOM_SORTED_TO_CODEC.items():
        if first_line.startswith(bom):
            return codec

    raise ValueError("No BOM found. Could not detect Unicode codec.")

