
def show_best_practices(file=sys.stdout) -> Union[str, None]:
    """
    Load and return the project's best practices.

    Example::

        >>> import pyparsing as pp
        >>> pp.show_best_practices()
        <!--
        This file contains instructions for best practices for developing parsers with pyparsing, and can be used by AI agents
        when generating Python code using pyparsing.
        -->
        ...

    This can also be run from the command line::

        python -m pyparsing.ai.show_best_practices
    """
    try:
        path = resources.files(__package__).joinpath("ai/best_practices.md")
        with path.open("r", encoding="utf-8") as f:
            content = f.read()
    except (FileNotFoundError, OSError):
        content = _FALLBACK_BEST_PRACTICES

    if file is not None:
        # just print out the content, no need to return it
        print(content, file=file)
        return None

    # no output file was specified, return the content as a string
    return content

