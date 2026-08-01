
def float32_ma():
    """Machine arithmetic parameters for float32."""
    f32 = ntypes.float32
    return MachArLike(f32,
                      machep=-23,
                      negep=-24,
                      minexp=-126,
                      maxexp=128,
                      nmant=23,
                      iexp=8)

