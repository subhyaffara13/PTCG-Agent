
def downgrade_cell(cell):
    """downgrade a cell from v4 to v3

    code cell:
        - set cell.language
        - cell.input <- cell.source
        - cell.prompt_number <- cell.execution_count
        - update outputs
    markdown cell:
        - single-line heading -> heading cell
    """
    if cell.cell_type == "code":
        cell.language = "python"
        cell.input = cell.pop("source", "")
        cell.prompt_number = cell.pop("execution_count", None)
        cell.collapsed = cell.metadata.pop("collapsed", False)
        cell.outputs = downgrade_outputs(cell.outputs)
    elif cell.cell_type == "markdown":
        source = cell.get("source", "")
        if "\n" not in source and source.startswith("#"):
            match = re.match(r"(#+)\s*(.*)", source)
            assert match is not None
            prefix, text = match.groups()
            cell.cell_type = "heading"
            cell.source = text
            cell.level = len(prefix)
    cell.pop("id", None)
    cell.pop("attachments", None)
    return cell

