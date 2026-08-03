from typing import Optional

def _fetchImageFileName(glif: bytes) -> Optional[str]:
    """
    The image file name (if any) from glif.
    """
    parser = _FetchImageFileNameParser()
    try:
        parser.parse(glif)
    except _DoneParsing:
        pass
    return parser.fileName

