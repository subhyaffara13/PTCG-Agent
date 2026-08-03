import sys

def is_interactive():
    """
    Return whether to redraw after every plotting command.

    .. note::

        This function is only intended for use in backends. End users should
        use `.pyplot.isinteractive` instead.
    """
    return rcParams['interactive']


def is_interactive():
    """Check if we are in an interractive environment.

    Override this function with a different logic if you are using this library
    outside a CLI.

    If the rapt token needs refreshing, the user needs to answer the challenges.
    If the user is not in an interractive environment, the challenges can not
    be answered and we just wait for timeout for no reason.

    Returns:
        bool: True if is interactive environment, False otherwise.
    """

    return sys.stdin.isatty()

