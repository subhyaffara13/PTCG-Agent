
def float64_ma():
    """Machine arithmetic parameters for float64."""
    f64 = ntypes.float64
    return MachArLike(f64,
                      machep=-52,
                      negep=-53,
                      minexp=-1022,
                      maxexp=1024,
                      nmant=52,
                      iexp=11)

