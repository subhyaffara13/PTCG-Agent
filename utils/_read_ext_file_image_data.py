
def _readExtFileImageData(bitmapObject, name, attrs, content, ttFont):
    fullPath = attrs["value"]
    with open(fullPath, "rb") as file:
        bitmapObject.imageData = file.read()

