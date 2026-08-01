
def _evaluate_argcomplete(parser: JupyterParser) -> list[str]:
    """If argcomplete is enabled, trigger autocomplete or return current words

    If the first word looks like a subcommand, return the current command
    that is attempting to be completed so that the subcommand can evaluate it;
    otherwise auto-complete using the main parser.
    """
    try:
        # traitlets >= 5.8 provides some argcomplete support,
        # use helper methods to jump to argcomplete
        from traitlets.config.argcomplete_config import (  # noqa: PLC0415
            get_argcomplete_cwords,
            increment_argcomplete_index,
        )

        cwords = get_argcomplete_cwords()
        if cwords and len(cwords) > 1 and not cwords[1].startswith("-"):
            # If first completion word looks like a subcommand,
            # increment word from which to start handling arguments
            increment_argcomplete_index()
            return cwords
        # Otherwise no subcommand, directly autocomplete and exit
        parser.argcomplete()
    except ImportError:
        # traitlets >= 5.8 not available, just try to complete this without
        # worrying about subcommands
        parser.argcomplete()
    msg = "Control flow should not reach end of autocomplete()"
    raise AssertionError(msg)

