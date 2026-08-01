
def notebook_to_myst(
    nb,
    code_directive=CODE_DIRECTIVE,
    raw_directive=RAW_DIRECTIVE,
    default_lexer=None,
):
    """Parse a notebook to a MyST formatted text document.

    :param nb: the notebook to parse
    :param code_directive: the name of the directive to use for code cells
    :param raw_directive: the name of the directive to use for raw cells
    :param default_lexer: a lexer name to use for annotating code cells
        (if ``nb.metadata.language_info.pygments_lexer`` is not available)
    """
    raise_if_myst_is_not_available()
    string = ""

    nb_metadata = nb.metadata

    # we add the pygments lexer as a directive argument, for use by syntax highlighters
    pygments_lexer = nb_metadata.get("language_info", {}).get("pygments_lexer", None)
    if pygments_lexer is None:
        pygments_lexer = default_lexer

    if nb_metadata:
        string += dump_yaml_blocks(nb_metadata, compact=False)

    last_cell_md = False
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == "markdown":
            metadata = cell.metadata
            if metadata or last_cell_md:
                if metadata:
                    string += f"\n+++ {json.dumps(metadata)}\n"
                else:
                    string += "\n+++\n"
            string += "\n" + cell.source
            if not cell.source.endswith("\n"):
                string += "\n"
            last_cell_md = True

        elif cell.cell_type in ["code", "raw"]:
            cell_delimiter = three_backticks_or_more(cell.source.splitlines())
            string += "\n{}{}".format(
                cell_delimiter,
                code_directive if cell.cell_type == "code" else raw_directive,
            )
            if pygments_lexer and cell.cell_type == "code":
                string += f" {pygments_lexer}"
            string += "\n"
            metadata = cell.metadata
            if metadata:
                string += dump_yaml_blocks(metadata)
            elif cell.source.startswith("---") or cell.source.startswith(":"):
                string += "\n"
            string += cell.source
            if not cell.source.endswith("\n"):
                string += "\n"
            string += cell_delimiter + "\n"
            last_cell_md = False

        else:
            raise NotImplementedError(f"cell {i}, type: {cell.cell_type}")

    if not nb_metadata:
        # remove initial blank line
        assert string.startswith("\n")
        string = string[1:]

    return string.rstrip() + "\n"

