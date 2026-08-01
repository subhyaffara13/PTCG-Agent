
def getsourcelines(object, lstrip=False, enclosing=False):
    """Return a list of source lines and starting line number for an object.
    Interactively-defined objects refer to lines in the interpreter's history.

    The argument may be a module, class, method, function, traceback, frame,
    or code object.  The source code is returned as a list of the lines
    corresponding to the object and the line number indicates where in the
    original source file the first line of code was found.  An IOError is
    raised if the source code cannot be retrieved, while a TypeError is
    raised for objects where the source code is unavailable (e.g. builtins).

    If lstrip=True, ensure there is no indentation in the first line of code.
    If enclosing=True, then also return any enclosing code."""
    code, n = getblocks(object, lstrip=lstrip, enclosing=enclosing, locate=True)
    return code[-1], n[-1]

