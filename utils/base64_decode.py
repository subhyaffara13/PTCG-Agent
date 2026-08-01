
def base64_decode(string: str | bytes) -> bytes:
    """Base64 decode a URL-safe string of bytes or text. The result is
    bytes.
    """
    string = want_bytes(string, encoding="ascii", errors="ignore")
    string += b"=" * (-len(string) % 4)

    try:
        return base64.urlsafe_b64decode(string)
    except (TypeError, ValueError) as e:
        raise BadData("Invalid base64-encoded data") from e


def base64_decode(nb):
    """Restore all bytes objects in the notebook from base64-encoded strings.

    Note: This is never used
    """
    for ws in nb.worksheets:
        for cell in ws.cells:
            if cell.cell_type == "code":
                for output in cell.outputs:
                    if "png" in output:
                        if isinstance(output.png, str):
                            output.png = output.png.encode("ascii")
                        output.png = decodebytes(output.png)
                    if "jpeg" in output:
                        if isinstance(output.jpeg, str):
                            output.jpeg = output.jpeg.encode("ascii")
                        output.jpeg = decodebytes(output.jpeg)
    return nb


def base64_decode(nb):
    """Restore all bytes objects in the notebook from base64-encoded strings.

    Note: This is never used
    """
    for ws in nb.worksheets:
        for cell in ws.cells:
            if cell.cell_type == "code":
                for output in cell.outputs:
                    if "png" in output:
                        if isinstance(output.png, str):
                            output.png = output.png.encode("ascii")
                        output.png = decodebytes(output.png)
                    if "jpeg" in output:
                        if isinstance(output.jpeg, str):
                            output.jpeg = output.jpeg.encode("ascii")
                        output.jpeg = decodebytes(output.jpeg)
    return nb

