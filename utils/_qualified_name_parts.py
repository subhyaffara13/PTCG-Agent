
def _qualified_name_parts(qualified_module_name: str) -> list[str]:
    """Split the names of the given module into subparts.

    For example,
        _qualified_name_parts('pylint.checkers.ImportsChecker')
    returns
        ['pylint', 'pylint.checkers', 'pylint.checkers.ImportsChecker']
    """
    names = qualified_module_name.split(".")
    return [".".join(names[0 : i + 1]) for i in range(len(names))]

