
def should_ignore_regular_constraints(options: Values) -> bool:
    """
    Check if regular constraints should be ignored because
    we are in a isolated build process and build constraints
    feature is enabled but no build constraints were passed.
    """

    return os.environ.get("_PIP_IN_BUILD_IGNORE_CONSTRAINTS") == "1"

