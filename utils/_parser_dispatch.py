
def _parser_dispatch(flavor: HTMLFlavors | None) -> type[_HtmlFrameParser]:
    """
    Choose the parser based on the input flavor.

    Parameters
    ----------
    flavor : {"lxml", "html5lib", "bs4"} or None
        The type of parser to use. This must be a valid backend.

    Returns
    -------
    cls : _HtmlFrameParser subclass
        The parser class based on the requested input flavor.

    Raises
    ------
    ValueError
        * If `flavor` is not a valid backend.
    ImportError
        * If you do not have the requested `flavor`
    """
    valid_parsers = list(_valid_parsers.keys())
    if flavor not in valid_parsers:
        raise ValueError(
            f"{flavor!r} is not a valid flavor, valid flavors are {valid_parsers}"
        )

    if flavor in ("bs4", "html5lib"):
        import_optional_dependency("html5lib")
        import_optional_dependency("bs4")
    else:
        import_optional_dependency("lxml.etree")
    return _valid_parsers[flavor]

