
def encoding_and_executable(notebook, metadata, ext):
    """Return encoding and executable lines for a notebook, if applicable"""
    lines = []
    comment = _SCRIPT_EXTENSIONS.get(ext, {}).get("comment")
    jupytext_metadata = metadata.get("jupytext", {})

    if comment is not None and "executable" in jupytext_metadata:
        lines.append("#!" + jupytext_metadata.pop("executable"))

    if comment is not None:
        if "encoding" in jupytext_metadata:
            lines.append(jupytext_metadata.pop("encoding"))
        elif default_language_from_metadata_and_ext(metadata, ext) != "python":
            for cell in notebook.cells:
                try:
                    cell.source.encode("ascii")
                except (UnicodeEncodeError, UnicodeDecodeError):
                    lines.append(comment + _UTF8_HEADER)
                    break

    return lines

