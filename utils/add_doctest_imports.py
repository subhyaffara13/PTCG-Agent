
def add_doctest_imports(doctest_namespace) -> None:
    """
    Make `np` and `pd` names available for doctests.
    """
    doctest_namespace["np"] = np
    doctest_namespace["pd"] = pd

