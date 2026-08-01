
def split_lines(nb):
    """split likely multiline text into lists of strings

    For file output more friendly to line-based VCS. ``rejoin_lines(nb)`` will
    reverse the effects of ``split_lines(nb)``.

    Used when writing JSON files.
    """
    for ws in nb.worksheets:
        for cell in ws.cells:
            if cell.cell_type == "code":
                if "input" in cell and isinstance(cell.input, str):
                    cell.input = cell.input.splitlines()
                for output in cell.outputs:
                    for key in _multiline_outputs:
                        item = output.get(key, None)
                        if isinstance(item, str):
                            output[key] = item.splitlines()
            else:  # text cell
                for key in ["source", "rendered"]:
                    item = cell.get(key, None)
                    if isinstance(item, str):
                        cell[key] = item.splitlines()
    return nb


def split_lines(nb):
    """split likely multiline text into lists of strings

    For file output more friendly to line-based VCS. ``rejoin_lines(nb)`` will
    reverse the effects of ``split_lines(nb)``.

    Used when writing JSON files.
    """
    for ws in nb.worksheets:
        for cell in ws.cells:
            if cell.cell_type == "code":
                if "input" in cell and isinstance(cell.input, str):
                    cell.input = cell.input.splitlines(True)
                for output in cell.outputs:
                    for key in _multiline_outputs:
                        item = output.get(key, None)
                        if isinstance(item, str):
                            output[key] = item.splitlines(True)
            else:  # text, heading cell
                for key in ["source", "rendered"]:
                    item = cell.get(key, None)
                    if isinstance(item, str):
                        cell[key] = item.splitlines(True)
    return nb


def split_lines(nb):
    """split likely multiline text into lists of strings

    For file output more friendly to line-based VCS. ``rejoin_lines(nb)`` will
    reverse the effects of ``split_lines(nb)``.

    Used when writing JSON files.
    """
    for cell in nb.cells:
        source = cell.get("source", None)
        if isinstance(source, str):
            cell["source"] = source.splitlines(True)

        attachments = cell.get("attachments", {})
        for _, attachment in attachments.items():
            _split_mimebundle(attachment)

        if cell.cell_type == "code":
            for output in cell.outputs:
                if output.output_type in {"execute_result", "display_data"}:
                    _split_mimebundle(output.get("data", {}))
                elif output.output_type == "stream" and isinstance(output.text, str):
                    output.text = output.text.splitlines(True)
    return nb


def split_lines(*streams: bytes) -> list[str]:
    """Returns a single list of string lines from the byte streams in args."""
    return [s for stream in streams for s in stream.decode("utf8").splitlines()]

