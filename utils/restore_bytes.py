
def restore_bytes(nb):
    """Restore bytes of image data from unicode-only formats.

    Base64 encoding is handled elsewhere.  Bytes objects in the notebook are
    always b64-encoded. We DO NOT encode/decode around file formats.
    """
    for ws in nb.worksheets:
        for cell in ws.cells:
            if cell.cell_type == "code":
                for output in cell.outputs:
                    if "png" in output:
                        output.png = output.png.encode("ascii")
                    if "jpeg" in output:
                        output.jpeg = output.jpeg.encode("ascii")
    return nb


def restore_bytes(nb):
    """Restore bytes of image data from unicode-only formats.

    Base64 encoding is handled elsewhere.  Bytes objects in the notebook are
    always b64-encoded. We DO NOT encode/decode around file formats.

    Note: this is never used
    """
    for ws in nb.worksheets:
        for cell in ws.cells:
            if cell.cell_type == "code":
                for output in cell.outputs:
                    if "png" in output:
                        output.png = output.png.encode("ascii", "replace")
                    if "jpeg" in output:
                        output.jpeg = output.jpeg.encode("ascii", "replace")
    return nb

