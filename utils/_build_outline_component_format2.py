
def _buildOutlineComponentFormat2(
    pen: AbstractPointPen, component: ElementType, identifiers: set[str], validate: bool
) -> None:
    if validate:
        if len(component):
            raise GlifLibError("Unknown child elements of component element.")
        for attr in component.attrib.keys():
            if attr not in componentAttributesFormat2:
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
    identifier = component.get("identifier")
    if identifier is not None:
        if validate:
            if identifier in identifiers:
                raise GlifLibError(
                    "The identifier %s is used more than once." % identifier
                )
            if validate and not identifierValidator(identifier):
                raise GlifLibError("The identifier %s is not valid." % identifier)
        identifiers.add(identifier)
    try:
        pen.addComponent(baseGlyphName, transformation, identifier=identifier)
    except TypeError:
        pen.addComponent(baseGlyphName, transformation)
        warn(
            "The addComponent method needs an identifier kwarg. The component's identifier value has been discarded.",
            DeprecationWarning,
        )

