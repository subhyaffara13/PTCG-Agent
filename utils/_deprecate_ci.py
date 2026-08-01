
def _deprecate_ci(errorbar, ci):
    """
    Warn on usage of ci= and convert to appropriate errorbar= arg.

    ci was deprecated when errorbar was added in 0.12. It should not be removed
    completely for some time, but it can be moved out of function definitions
    (and extracted from kwargs) after one cycle.

    """
    if ci is not deprecated and ci != "deprecated":
        if ci is None:
            errorbar = None
        elif ci == "sd":
            errorbar = "sd"
        else:
            errorbar = ("ci", ci)
        msg = (
            "\n\nThe `ci` parameter is deprecated. "
            f"Use `errorbar={repr(errorbar)}` for the same effect.\n"
        )
        warnings.warn(msg, FutureWarning, stacklevel=3)

    return errorbar

