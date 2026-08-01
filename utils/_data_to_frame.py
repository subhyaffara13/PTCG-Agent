
def _data_to_frame(**kwargs):
    head, body, foot = kwargs.pop("data")
    header = kwargs.pop("header")
    kwargs["skiprows"] = _get_skiprows(kwargs["skiprows"])
    if head:
        body = head + body

        # Infer header when there is a <thead> or top <th>-only rows
        if header is None:
            if len(head) == 1:
                header = 0
            else:
                # ignore all-empty-text rows
                header = [i for i, row in enumerate(head) if any(text for text in row)]

    if foot:
        body += foot

    # fill out elements of body that are "ragged"
    _expand_elements(body)
    with TextParser(body, header=header, **kwargs) as tp:
        return tp.read()


def _data_to_frame(data: list[dict[str, str | None]], **kwargs) -> DataFrame:
    """
    Convert parsed data to Data Frame.

    This method will bind xml dictionary data of keys and values
    into named columns of Data Frame using the built-in TextParser
    class that build Data Frame and infers specific dtypes.
    """

    tags = next(iter(data))
    nodes = [list(d.values()) for d in data]

    try:
        with TextParser(nodes, names=tags, **kwargs) as tp:
            return tp.read()
    except ParserError as err:
        raise ParserError(
            "XML document may be too complex for import. "
            "Try to flatten document and use distinct "
            "element and attribute names."
        ) from err

