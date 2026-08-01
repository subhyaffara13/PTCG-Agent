
def extract_commutative(kron):
    c_part = []
    nc_part = []
    for arg in kron.args:
        c, nc = arg.args_cnc()
        c_part.extend(c)
        nc_part.append(Mul._from_args(nc))

    c_part = Mul(*c_part)
    if c_part != 1:
        return c_part*KroneckerProduct(*nc_part)
    return kron

