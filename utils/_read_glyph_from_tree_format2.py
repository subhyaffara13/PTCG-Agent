
def _readGlyphFromTreeFormat2(
    tree: ElementType,
    glyphObject: Optional[Any] = None,
    pointPen: Optional[AbstractPointPen] = None,
    validate: bool = False,
    formatMinor: int = 0,
) -> None:
    # get the name
    _readName(glyphObject, tree, validate)
    # populate the sub elements
    unicodes = []
    guidelines = []
    anchors = []
    haveSeenAdvance = haveSeenImage = haveSeenOutline = haveSeenLib = haveSeenNote = (
        False
    )
    identifiers: set[str] = set()
    for element in tree:
        if element.tag == "outline":
            if validate:
                if haveSeenOutline:
                    raise GlifLibError("The outline element occurs more than once.")
                if element.attrib:
                    raise GlifLibError(
                        "The outline element contains unknown attributes."
                    )
                if element.text and element.text.strip() != "":
                    raise GlifLibError("Invalid outline structure.")
            haveSeenOutline = True
            if pointPen is not None:
                buildOutlineFormat2(
                    glyphObject, pointPen, element, identifiers, validate
                )
        elif glyphObject is None:
            # Skip remaining elements if no glyphObject, but outline is still
            # processed above to allow drawing via pointPen without a glyphObject.
            continue
        elif element.tag == "advance":
            if validate and haveSeenAdvance:
                raise GlifLibError("The advance element occurs more than once.")
            haveSeenAdvance = True
            _readAdvance(glyphObject, element)
        elif element.tag == "unicode":
            v = element.get("hex")
            if v is None:
                raise GlifLibError(
                    "A unicode element is missing its required hex attribute."
                )
            try:
                v = int(v, 16)
                if v not in unicodes:
                    unicodes.append(v)
            except ValueError:
                raise GlifLibError(
                    "Illegal value for hex attribute of unicode element."
                )
        elif element.tag == "guideline":
            if validate and len(element):
                raise GlifLibError("Unknown children in guideline element.")
            attrib = dict(element.attrib)
            for attr in ("x", "y", "angle"):
                if attr in attrib:
                    attrib[attr] = _number(attrib[attr])
            guidelines.append(attrib)
        elif element.tag == "anchor":
            if validate and len(element):
                raise GlifLibError("Unknown children in anchor element.")
            attrib = dict(element.attrib)
            for attr in ("x", "y"):
                if attr in element.attrib:
                    attrib[attr] = _number(attrib[attr])
            anchors.append(attrib)
        elif element.tag == "image":
            if validate:
                if haveSeenImage:
                    raise GlifLibError("The image element occurs more than once.")
                if len(element):
                    raise GlifLibError("Unknown children in image element.")
            haveSeenImage = True
            _readImage(glyphObject, element, validate)
        elif element.tag == "note":
            if validate and haveSeenNote:
                raise GlifLibError("The note element occurs more than once.")
            haveSeenNote = True
            _readNote(glyphObject, element)
        elif element.tag == "lib":
            if validate and haveSeenLib:
                raise GlifLibError("The lib element occurs more than once.")
            haveSeenLib = True
            _readLib(glyphObject, element, validate)
        else:
            raise GlifLibError("Unknown element in GLIF: %s" % element)
    # set the collected unicodes
    if unicodes:
        _relaxedSetattr(glyphObject, "unicodes", unicodes)
    # set the collected guidelines
    if guidelines:
        if validate and not guidelinesValidator(guidelines, identifiers):
            raise GlifLibError("The guidelines are improperly formatted.")
        _relaxedSetattr(glyphObject, "guidelines", guidelines)
    # set the collected anchors
    if anchors:
        if validate and not anchorsValidator(anchors, identifiers):
            raise GlifLibError("The anchors are improperly formatted.")
        _relaxedSetattr(glyphObject, "anchors", anchors)

