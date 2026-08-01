
def _bytes_to_image(content: bytes) -> "Image":
    """Parse bytes from a Response object into a PIL Image.

    Expects the response body to be raw bytes. To deal with b64 encoded images, use `_b64_to_image` instead.
    """
    Image = _import_pil_image()
    return Image.open(io.BytesIO(content))

