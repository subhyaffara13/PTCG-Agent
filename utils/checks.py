
def checks(*args):
    """Decorator function to set checks to be run."""

    def wrapper(func):
        if not hasattr(func, "_checks"):
            func._checks = []
        for arg in args:
            if arg == "File":
                func._checks.append("File")
            else:
                func._checks.append(utils.check_ast_node(arg))

        LOG.debug("checks() decorator executed")
        LOG.debug("  func._checks: %s", func._checks)
        return func

    return wrapper

