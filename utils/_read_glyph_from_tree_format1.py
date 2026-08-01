
def _readGlyphFromTreeFormat1(
    tree: ElementType,
    glyphObject: Optional[Any] = None,
    pointPen: Optional[AbstractPointPen] = None,
    validate: bool = False,
    **kwargs: Any,
) -> None:
    # get the name
    _readName(glyphObject, tree, validate)
    # populate the sub elements
    unicodes = []
    haveSeenAdvance = haveSeenOutline = haveSeenLib = haveSeenNote = False
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
            buildOutlineFormat1(glyphObject, pointPen, element, validate)
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

