
def f2cexpr(expr):
    """Rewrite Fortran expression as f2py supported C expression.

    Due to the lack of a proper expression parser in f2py, this
    function uses a heuristic approach that assumes that Fortran
    arithmetic expressions are valid C arithmetic expressions when
    mapping Fortran function calls to the corresponding C function/CPP
    macros calls.

    """
    # TODO: support Fortran `len` function with optional kind parameter
    expr = re.sub(r'\blen\b', 'f2py_slen', expr)
    return expr

