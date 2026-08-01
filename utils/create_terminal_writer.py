
def create_terminal_writer(
    config: Config, file: TextIO | None = None
) -> TerminalWriter:
    """Create a TerminalWriter instance configured according to the options
    in the config object.

    Every code which requires a TerminalWriter object and has access to a
    config object should use this function.
    """
    tw = TerminalWriter(file=file)

    if config.option.color == "yes":
        tw.hasmarkup = True
    elif config.option.color == "no":
        tw.hasmarkup = False

    if config.option.code_highlight == "yes":
        tw.code_highlight = True
    elif config.option.code_highlight == "no":
        tw.code_highlight = False

    return tw

