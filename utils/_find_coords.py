
def _find_coords(expr):
    # Finds CoordinateSystems existing in expr
    fields = expr.atoms(BaseScalarField, BaseVectorField)
    return {f._coord_sys for f in fields}

