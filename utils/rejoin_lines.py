
def rejoin_lines(nb):
    """rejoin multiline text into strings

    For reversing effects of ``split_lines(nb)``.

    This only rejoins lines that have been split, so if text objects were not split
    they will pass through unchanged.

    Used when reading JSON files that may have been passed through split_lines.
    """
    for ws in nb.worksheets:
        for cell in ws.cells:
            if cell.cell_type == "code":
                if "input" in cell and isinstance(cell.input, list):
                    cell.input = "\n".join(cell.input)
                for output in cell.outputs:
                    for key in _multiline_outputs:
                        item = output.get(key, None)
                        if isinstance(item, list):
                            output[key] = "\n".join(item)
            else:  # text cell
                for key in ["source", "rendered"]:
                    item = cell.get(key, None)
                    if isinstance(item, list):
                        cell[key] = "\n".join(item)
    return nb


def rejoin_lines(nb):
    """rejoin multiline text into strings

    For reversing effects of ``split_lines(nb)``.

    This only rejoins lines that have been split, so if text objects were not split
    they will pass through unchanged.

    Used when reading JSON files that may have been passed through split_lines.
    """
    for ws in nb.worksheets:
        for cell in ws.cells:
            if cell.cell_type == "code":
                if "input" in cell and isinstance(cell.input, list):
                    cell.input = _join_lines(cell.input)
                for output in cell.outputs:
                    for key in _multiline_outputs:
                        item = output.get(key, None)
                        if isinstance(item, list):
                            output[key] = _join_lines(item)
            else:  # text, heading cell
                for key in ["source", "rendered"]:
                    item = cell.get(key, None)
                    if isinstance(item, list):
                        cell[key] = _join_lines(item)
    return nb


def rejoin_lines(nb):
    """rejoin multiline text into strings

    For reversing effects of ``split_lines(nb)``.

    This only rejoins lines that have been split, so if text objects were not split
    they will pass through unchanged.

    Used when reading JSON files that may have been passed through split_lines.
    """
    for cell in nb.cells:
        if "source" in cell and isinstance(cell.source, list):
            cell.source = "".join(cell.source)

        attachments = cell.get("attachments", {})
        for _, attachment in attachments.items():
            _rejoin_mimebundle(attachment)

        if cell.get("cell_type", None) == "code":
            for output in cell.get("outputs", []):
                output_type = output.get("output_type", "")
                if output_type in {"execute_result", "display_data"}:
                    _rejoin_mimebundle(output.get("data", {}))
                elif output_type and isinstance(output.get("text", ""), list):
                    output.text = "".join(output.text)
    return nb

