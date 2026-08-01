
def _validate_bc_type(bc_type):
    if bc_type is None:
        return "not-a-knot"

    if bc_type not in ("not-a-knot", "periodic"):
        raise ValueError("Only 'not-a-knot' and 'periodic' "
                         "boundary conditions are recognised, "
                         f"found {bc_type}")

    return bc_type

