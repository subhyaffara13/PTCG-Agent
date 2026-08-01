
def _readImage(glyphObject: Optional[Any], image: ElementType, validate: bool) -> None:
    imageData = dict(image.attrib)
    for attr, default in _transformationInfo:
        value = imageData.get(attr, default)
        imageData[attr] = _number(value)
    if validate and not imageValidator(imageData):
        raise GlifLibError("The image element is not properly formatted.")
    _relaxedSetattr(glyphObject, "image", imageData)

