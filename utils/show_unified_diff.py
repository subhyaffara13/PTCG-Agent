from pathlib import Path


def show_unified_diff(
    *,
    file_input: str,
    file_output: str,
    file_path: Path | None,
    output: TextIO | None = None,
    color_output: bool = False,
) -> None:
    """Shows a unified_diff for the provided input and output against the provided file path.

    - **file_input**: A string that represents the contents of a file before changes.
    - **file_output**: A string that represents the contents of a file after changes.
    - **file_path**: A Path object that represents the file path of the file being changed.
    - **output**: A stream to output the diff to. If non is provided uses sys.stdout.
    - **color_output**: Use color in output if True.
    """
    printer = create_terminal_printer(color_output, output)
    file_name = "" if file_path is None else str(file_path)
    file_mtime = str(
        datetime.now() if file_path is None else datetime.fromtimestamp(file_path.stat().st_mtime)
    )
    unified_diff_lines = unified_diff(
        file_input.splitlines(keepends=True),
        file_output.splitlines(keepends=True),
        fromfile=file_name + ":before",
        tofile=file_name + ":after",
        fromfiledate=file_mtime,
        tofiledate=str(datetime.now()),
    )
    for line in unified_diff_lines:
        printer.diff_line(line)

