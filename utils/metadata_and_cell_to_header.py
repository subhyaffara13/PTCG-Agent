
def metadata_and_cell_to_header(notebook, metadata, text_format, fmt, unsupported_keys=None):
    """
    Return the text header corresponding to a notebook, and remove the
    first cell of the notebook if it contained the header
    """

    header = []

    lines_to_next_cell = None
    root_level_metadata = {}
    root_level_metadata_as_raw_cell = fmt.get("root_level_metadata_as_raw_cell", True)

    if not root_level_metadata_as_raw_cell:
        root_level_metadata = metadata.get("jupytext", {}).pop("root_level_metadata", {})
    elif notebook.cells:
        cell = notebook.cells[0]
        if cell.cell_type == "raw":
            lines = cell.source.strip("\n\t ").splitlines()
            if len(lines) >= 2 and _HEADER_RE.match(lines[0]) and _HEADER_RE.match(lines[-1]):
                header = lines[1:-1]
                lines_to_next_cell = cell.metadata.get("lines_to_next_cell")
                notebook.cells = notebook.cells[1:]

    metadata = insert_jupytext_info_and_filter_metadata(metadata, fmt, text_format, unsupported_keys)

    if metadata:
        root_level_metadata["jupyter"] = metadata

    if root_level_metadata:
        header.extend(yaml.safe_dump(root_level_metadata, default_flow_style=False).splitlines())

    if header:
        header = ["---"] + header + ["---"]

        if fmt.get("hide_notebook_metadata", False) and text_format.format_name == "markdown":
            header = ["<!--", ""] + header + ["", "-->"]

    return (
        comment_lines(header, text_format.header_prefix, text_format.header_suffix),
        lines_to_next_cell,
    )

