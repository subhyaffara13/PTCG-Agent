
def read_pair(inputs, outputs, read_one_file, must_match=False):
    """Read a notebook given its inputs and outputs path and formats"""
    if not outputs.path or outputs.path == inputs.path:
        return read_one_file(inputs.path, inputs.fmt)

    notebook = read_one_file(inputs.path, inputs.fmt)
    check_file_version(notebook, inputs.path, outputs.path)

    notebook_with_outputs = read_one_file(outputs.path, outputs.fmt)

    if must_match:
        in_text = jupytext.writes(notebook, inputs.fmt)
        out_text = jupytext.writes(notebook_with_outputs, inputs.fmt)
        diff = compare(out_text, in_text, outputs.path, inputs.path, return_diff=True)
        if diff:
            raise PairedFilesDiffer(diff)

    notebook = combine_inputs_with_outputs(
        notebook, notebook_with_outputs, fmt=inputs.fmt
    )

    return notebook

