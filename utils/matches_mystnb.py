
def matches_mystnb(
    text,
    ext=None,
    requires_meta=True,
    code_directive=CODE_DIRECTIVE,
    raw_directive=RAW_DIRECTIVE,
):
    """Attempt to distinguish a file as myst, only given its extension and content.

    :param ext: the extension of the file
    :param requires_meta: requires the file to contain top matter metadata
    :param code_directive: the name of the directive to search for containing code cells
    :param raw_directive: the name of the directive to search for containing raw cells
    """
    # is the extension uniquely associated with myst (i.e. not just .md)
    if ext and "." + ("." + ext).rsplit(".", 1)[1] in myst_extensions(no_md=True):
        return True

    # might the text contain metadata front matter
    if requires_meta and not text.startswith("---"):
        return False

    try:
        tokens = get_parser().parse(text + "\n")
    except (TypeError, ValueError) as err:
        warnings.warn(f"myst-parser failed unexpectedly: {err}")  # pragma: no cover
        return False

    # Is the format information available in the jupytext text representation?
    if tokens and tokens[0].type == "front_matter":
        try:
            metadata = yaml.safe_load(tokens[0].content)
        except (yaml.parser.ParserError, yaml.scanner.ScannerError):
            pass
        else:
            try:
                format_name = (
                    metadata.get(_JUPYTER_METADATA_NAMESPACE, metadata)
                    .get("jupytext", {})
                    .get("text_representation", {})
                    .get("format_name")
                )
            except AttributeError:
                pass
            else:
                if format_name == MYST_FORMAT_NAME:
                    return True

    # is there at least on fenced code block with a code/raw directive language
    for token in tokens:
        if token.type == "fence" and (token.info.startswith(code_directive) or token.info.startswith(raw_directive)):
            return True

    return False

