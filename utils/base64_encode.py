
def base64_encode(string: str | bytes) -> bytes:
    """Base64 encode a string of bytes or text. The resulting bytes are
    safe to use in URLs.
    """
    string = want_bytes(string)
    return base64.urlsafe_b64encode(string).rstrip(b"=")


def base64_encode(nb):
    """Base64 encode all bytes objects in the notebook.

    These will be b64-encoded unicode strings

    Note: This is never used
    """
    for ws in nb.worksheets:
        for cell in ws.cells:
            if cell.cell_type == "code":
                for output in cell.outputs:
                    if "png" in output:
                        output.png = encodebytes(output.png).decode("ascii")
                    if "jpeg" in output:
                        output.jpeg = encodebytes(output.jpeg).decode("ascii")
    return nb


def base64_encode(nb):
    """Base64 encode all bytes objects in the notebook.

    These will be b64-encoded unicode strings

    Note: This is never used
    """
    for ws in nb.worksheets:
        for cell in ws.cells:
            if cell.cell_type == "code":
                for output in cell.outputs:
                    if "png" in output:
                        output.png = encodebytes(output.png).decode("ascii")
                    if "jpeg" in output:
                        output.jpeg = encodebytes(output.jpeg).decode("ascii")
    return nb

