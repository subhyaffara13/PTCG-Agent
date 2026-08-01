
def myst_to_notebook(
    text,
    code_directive=CODE_DIRECTIVE,
    raw_directive=RAW_DIRECTIVE,
    add_source_map=False,
):
    """Convert text written in the myst format to a notebook.

    :param text: the file text
    :param code_directive: the name of the directive to search for containing code cells
    :param raw_directive: the name of the directive to search for containing raw cells
    :param add_source_map: add a `source_map` key to the notebook metadata,
        which is a list of the starting source line number for each cell.

    :raises MystMetadataParsingError if the metadata block is not valid JSON/YAML

    NOTE: we assume here that all of these directives are at the top-level,
    i.e. not nested in other directives.
    """
    raise_if_myst_is_not_available()

    tokens = get_parser().parse(text + "\n")
    lines = text.splitlines()
    md_start_line = 0
    default_lexer = None

    # get the document metadata
    metadata_nb = {}
    if tokens and tokens[0].type == "front_matter":
        metadata = tokens.pop(0)
        md_start_line = metadata.map[1]
        try:
            metadata_nb = yaml.safe_load(metadata.content)
        except (yaml.parser.ParserError, yaml.scanner.ScannerError) as error:
            raise MystMetadataParsingError(f"Notebook metadata: {error}")

    # create an empty notebook
    nbf_version = nbf.v4
    kwargs = {"metadata": nbf.from_dict(metadata_nb)}
    notebook = nbf_version.new_notebook(**kwargs)
    source_map = []  # this is a list of the starting line number for each cell

    def _flush_markdown(start_line, token, md_metadata):
        """When we find a cell we check if there is preceding text.o"""
        endline = token.map[0] if token else len(lines)
        md_source = strip_blank_lines("\n".join(lines[start_line:endline]))
        meta = nbf.from_dict(md_metadata)
        if md_source:
            source_map.append(start_line)
            notebook.cells.append(nbf_version.new_markdown_cell(source=md_source, metadata=meta))

    # iterate through the tokens to identify notebook cells
    nesting_level = 0
    md_metadata = {}

    for token in tokens:
        nesting_level += token.nesting

        if nesting_level != 0:
            # we ignore fenced block that are nested, e.g. as part of lists, etc
            continue

        if token.type == "fence" and token.info.startswith(code_directive):
            _flush_markdown(md_start_line, token, md_metadata)
            options, body_lines = read_fenced_cell(token, len(notebook.cells), "Code")
            assert token.info.startswith(code_directive)
            lexer = token.info[len(code_directive) :].strip()
            if lexer:
                if not default_lexer:
                    default_lexer = lexer
                elif lexer != default_lexer:
                    warnings.warn(f"All code cells in a MyST notebook must have the same language: {lexer}!={default_lexer}")

            meta = nbf.from_dict(options)
            source_map.append(token.map[0] + 1)
            notebook.cells.append(nbf_version.new_code_cell(source="\n".join(body_lines), metadata=meta))
            md_metadata = {}
            md_start_line = token.map[1]

        elif token.type == "fence" and token.info.startswith(raw_directive):
            _flush_markdown(md_start_line, token, md_metadata)
            options, body_lines = read_fenced_cell(token, len(notebook.cells), "Raw")
            meta = nbf.from_dict(options)
            source_map.append(token.map[0] + 1)
            notebook.cells.append(nbf_version.new_raw_cell(source="\n".join(body_lines), metadata=meta))
            md_metadata = {}
            md_start_line = token.map[1]

        elif token.type == "myst_block_break":
            _flush_markdown(md_start_line, token, md_metadata)
            md_metadata = read_cell_metadata(token, len(notebook.cells))
            md_start_line = token.map[1]

    _flush_markdown(md_start_line, None, md_metadata)

    if add_source_map:
        notebook.metadata["source_map"] = source_map

    if "language_info" not in notebook.metadata and default_lexer:
        has_metadata = bool(notebook.metadata)
        jupyter_metadata = notebook.metadata.setdefault(_JUPYTER_METADATA_NAMESPACE, {})
        jupytext_metadata = jupyter_metadata.setdefault("jupytext", {})
        jupytext_metadata["default_lexer"] = default_lexer
        if not has_metadata:
            jupytext_metadata["notebook_metadata_filter"] = "-all"

    return notebook

