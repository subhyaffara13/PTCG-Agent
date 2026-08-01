
def _get_image_from_kw(kw: dict[str, Any]) -> ImageFile.ImageFile | None:
    source = None
    if "file" in kw:
        source = kw.pop("file")
    elif "data" in kw:
        source = BytesIO(kw.pop("data"))
    if not source:
        return None
    return Image.open(source)

