
def new_output(
    output_type=None,
    output_text=None,
    output_png=None,
    output_html=None,
    output_svg=None,
    output_latex=None,
    output_json=None,
    output_javascript=None,
    output_jpeg=None,
    prompt_number=None,
    etype=None,
    evalue=None,
    traceback=None,
):
    """Create a new code cell with input and output"""
    output = NotebookNode()
    if output_type is not None:
        output.output_type = str(output_type)

    if output_type != "pyerr":
        if output_text is not None:
            output.text = str(output_text)
        if output_png is not None:
            output.png = bytes(output_png)
        if output_jpeg is not None:
            output.jpeg = bytes(output_jpeg)
        if output_html is not None:
            output.html = str(output_html)
        if output_svg is not None:
            output.svg = str(output_svg)
        if output_latex is not None:
            output.latex = str(output_latex)
        if output_json is not None:
            output.json = str(output_json)
        if output_javascript is not None:
            output.javascript = str(output_javascript)

    if output_type == "pyout" and prompt_number is not None:
        output.prompt_number = int(prompt_number)

    if output_type == "pyerr":
        if etype is not None:
            output.etype = str(etype)
        if evalue is not None:
            output.evalue = str(evalue)
        if traceback is not None:
            output.traceback = [str(frame) for frame in list(traceback)]

    return output


def new_output(
    output_type,
    output_text=None,
    output_png=None,
    output_html=None,
    output_svg=None,
    output_latex=None,
    output_json=None,
    output_javascript=None,
    output_jpeg=None,
    prompt_number=None,
    ename=None,
    evalue=None,
    traceback=None,
    stream=None,
    metadata=None,
):
    """Create a new output, to go in the ``cell.outputs`` list of a code cell."""
    output = NotebookNode()
    output.output_type = str(output_type)

    if metadata is None:
        metadata = {}
    if not isinstance(metadata, dict):
        msg = "metadata must be dict"
        raise TypeError(msg)

    if output_type in {"pyout", "display_data"}:
        output.metadata = metadata

    if output_type != "pyerr":
        if output_text is not None:
            output.text = str_passthrough(output_text)
        if output_png is not None:
            output.png = cast_str(output_png)
        if output_jpeg is not None:
            output.jpeg = cast_str(output_jpeg)
        if output_html is not None:
            output.html = str_passthrough(output_html)
        if output_svg is not None:
            output.svg = str_passthrough(output_svg)
        if output_latex is not None:
            output.latex = str_passthrough(output_latex)
        if output_json is not None:
            output.json = str_passthrough(output_json)
        if output_javascript is not None:
            output.javascript = str_passthrough(output_javascript)

    if output_type == "pyout" and prompt_number is not None:
        output.prompt_number = int(prompt_number)

    if output_type == "pyerr":
        if ename is not None:
            output.ename = str_passthrough(ename)
        if evalue is not None:
            output.evalue = str_passthrough(evalue)
        if traceback is not None:
            output.traceback = [str_passthrough(frame) for frame in list(traceback)]

    if output_type == "stream":
        output.stream = "stdout" if stream is None else str_passthrough(stream)

    return output


def new_output(output_type, data=None, **kwargs):
    """Create a new output, to go in the ``cell.outputs`` list of a code cell."""
    output = NotebookNode(output_type=output_type)

    # populate defaults:
    if output_type == "stream":
        output.name = "stdout"
        output.text = ""
    elif output_type == "display_data":
        output.metadata = NotebookNode()
        output.data = NotebookNode()
    elif output_type == "execute_result":
        output.metadata = NotebookNode()
        output.data = NotebookNode()
        output.execution_count = None
    elif output_type == "error":
        output.ename = "NotImplementedError"
        output.evalue = ""
        output.traceback = []

    # load from args:
    output.update(kwargs)
    if data is not None:
        output.data = data
    # validate
    validate(output, output_type)
    return output

