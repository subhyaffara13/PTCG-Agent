
def _buildOutlineComponentFormat1(
    pen: AbstractPointPen, component: ElementType, validate: bool
) -> None:
    if validate:
        if len(component):
            raise GlifLibError("Unknown child elements of component element.")
        for attr in component.attrib.keys():
            if attr not in componentAttributesFormat1:
                raise GlifLibError("Unknown attribute in component element: %s" % attr)
    baseGlyphName = component.get("base")
    if validate and baseGlyphName is None:
        raise GlifLibError("The base attribute is not defined in the component.")
    assert baseGlyphName is not None
    transformation = tuple(
        _number(component.get(attr) or default) for attr, default in _transformationInfo
    )
    transformation = cast(
        tuple[float, float, float, float, float, float], transformation
    )
    pen.addComponent(baseGlyphName, transformation)

