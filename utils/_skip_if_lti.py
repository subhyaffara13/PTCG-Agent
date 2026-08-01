
def _skip_if_lti(arg):
    """Handle `system` arg overloads.

    ATM, only pass tuples through. Consider updating when cupyx.lti class
    is supported.
    """
    if isinstance(arg, tuple):
        return arg
    else:
        return (None,)

