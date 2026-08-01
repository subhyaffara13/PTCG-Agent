
def check_if_graphviz_supports_format(output_format: str) -> None:
    """Check if the ``dot`` command supports the requested output format.

    This is needed if image output is desired and ``dot`` is used to convert
    from *.gv into the final output format.
    """
    dot_output = subprocess.run(
        ["dot", "-T?"], capture_output=True, check=False, encoding="utf-8"
    )
    match = re.match(
        pattern=r".*Use one of: (?P<formats>(\S*\s?)+)",
        string=dot_output.stderr.strip(),
    )
    if not match:
        print(
            "Unable to determine Graphviz supported output formats. "
            "Pyreverse will continue, but subsequent error messages "
            "regarding the output format may come from Graphviz directly."
        )
        return
    supported_formats = match.group("formats")
    if output_format not in supported_formats.split():
        print(
            f"Format {output_format} is not supported by Graphviz. It supports: {supported_formats}"
        )
        sys.exit(32)

