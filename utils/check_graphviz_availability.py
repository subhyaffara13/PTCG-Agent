import sys

def check_graphviz_availability() -> None:
    """Check if the ``dot`` command is available on the machine.

    This is needed if image output is desired and ``dot`` is used to convert
    from *.dot or *.gv into the final output format.
    """
    if shutil.which("dot") is None:
        print("'Graphviz' needs to be installed for your chosen output format.")
        sys.exit(32)

