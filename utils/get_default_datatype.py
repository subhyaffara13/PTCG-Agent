
def get_default_datatype(expr, complex_allowed=None):
    """Derives an appropriate datatype based on the expression."""
    if complex_allowed is None:
        complex_allowed = COMPLEX_ALLOWED
    if complex_allowed:
        final_dtype = "complex"
    else:
        final_dtype = "float"
    if expr.is_integer:
        return default_datatypes["int"]
    elif expr.is_real:
        return default_datatypes["float"]
    elif isinstance(expr, MatrixBase):
        #check all entries
        dt = "int"
        for element in expr:
            if dt == "int" and not element.is_integer:
                dt = "float"
            if dt == "float" and not element.is_real:
                return default_datatypes[final_dtype]
        return default_datatypes[dt]
    else:
        return default_datatypes[final_dtype]

