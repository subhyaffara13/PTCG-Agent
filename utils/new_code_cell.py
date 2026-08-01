
def new_code_cell(code=None, prompt_number=None):
    """Create a new code cell with input and output"""
    cell = NotebookNode()
    cell.cell_type = "code"
    if code is not None:
        cell.code = str(code)
    if prompt_number is not None:
        cell.prompt_number = int(prompt_number)
    return cell


def new_code_cell(
    input=None,
    prompt_number=None,
    outputs=None,
    language="python",
    collapsed=False,
):
    """Create a new code cell with input and output"""
    cell = NotebookNode()
    cell.cell_type = "code"
    if language is not None:
        cell.language = str(language)
    if input is not None:
        cell.input = str(input)
    if prompt_number is not None:
        cell.prompt_number = int(prompt_number)
    if outputs is None:
        cell.outputs = []
    else:
        cell.outputs = outputs
    if collapsed is not None:
        cell.collapsed = bool(collapsed)

    return cell


def new_code_cell(
    input=None,
    prompt_number=None,
    outputs=None,
    language="python",
    collapsed=False,
    metadata=None,
):
    """Create a new code cell with input and output"""
    cell = NotebookNode()
    cell.cell_type = "code"
    if language is not None:
        cell.language = str_passthrough(language)
    if input is not None:
        cell.input = str_passthrough(input)
    if prompt_number is not None:
        cell.prompt_number = int(prompt_number)
    if outputs is None:
        cell.outputs = []
    else:
        cell.outputs = outputs
    if collapsed is not None:
        cell.collapsed = bool(collapsed)
    cell.metadata = NotebookNode(metadata or {})

    return cell


def new_code_cell(source="", **kwargs):
    """Create a new code cell"""
    cell = NotebookNode(
        id=random_cell_id(),
        cell_type="code",
        metadata=NotebookNode(),
        execution_count=None,
        source=source,
        outputs=[],
    )
    cell.update(kwargs)

    validate(cell, "code_cell")
    return cell

