
def get_sympy_dir():
    """
    Returns the root SymPy directory and set the global value
    indicating whether the system is case sensitive or not.
    """
    this_file = os.path.abspath(__file__)
    sympy_dir = os.path.join(os.path.dirname(this_file), "..", "..")
    sympy_dir = os.path.normpath(sympy_dir)
    return os.path.normcase(sympy_dir)

