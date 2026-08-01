
def parseString(
    string, namespaces=True, forbid_dtd=False, forbid_entities=True, forbid_external=True
):
    """Parse a document from a string, returning the resulting
    Document node.
    """
    if namespaces:
        build_builder = DefusedExpatBuilderNS
    else:
        build_builder = DefusedExpatBuilder
    builder = build_builder(
        forbid_dtd=forbid_dtd, forbid_entities=forbid_entities, forbid_external=forbid_external
    )
    return builder.parseString(string)


def parseString(
    string, parser=None, forbid_dtd=False, forbid_entities=True, forbid_external=True
):
    """Parse a file into a DOM from a string."""
    if parser is None:
        return _expatbuilder.parseString(
            string,
            forbid_dtd=forbid_dtd,
            forbid_entities=forbid_entities,
            forbid_external=forbid_external,
        )
    else:
        return _do_pulldom_parse(
            _pulldom.parseString,
            (string,),
            {
                "parser": parser,
                "forbid_dtd": forbid_dtd,
                "forbid_entities": forbid_entities,
                "forbid_external": forbid_external,
            },
        )


def parseString(
    string, parser=None, forbid_dtd=False, forbid_entities=True, forbid_external=True
):
    if parser is None:
        parser = make_parser()
        parser.forbid_dtd = forbid_dtd
        parser.forbid_entities = forbid_entities
        parser.forbid_external = forbid_external
    return _parseString(string, parser)


def parseString(
    string,
    handler,
    errorHandler=_ErrorHandler(),
    forbid_dtd=False,
    forbid_entities=True,
    forbid_external=True,
):
    from io import BytesIO

    if errorHandler is None:
        errorHandler = _ErrorHandler()
    parser = make_parser()
    parser.setContentHandler(handler)
    parser.setErrorHandler(errorHandler)
    parser.forbid_dtd = forbid_dtd
    parser.forbid_entities = forbid_entities
    parser.forbid_external = forbid_external

    inpsrc = _InputSource()
    inpsrc.setByteStream(BytesIO(string))
    parser.parse(inpsrc)

