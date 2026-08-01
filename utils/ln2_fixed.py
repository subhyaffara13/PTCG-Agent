
def ln2_fixed(prec):
    """
    Computes ln(2). This is done with a hyperbolic Machin-type formula,
    with binary splitting at high precision.
    """
    return machin([(18, 26), (-2, 4801), (8, 8749)], prec, True)

