
def float16_ma():
    """Machine arithmetic parameters for float16."""
    f16 = ntypes.float16
    return MachArLike(f16,
                      machep=-10,
                      negep=-11,
                      minexp=-14,
                      maxexp=16,
                      nmant=10,
                      iexp=5)

