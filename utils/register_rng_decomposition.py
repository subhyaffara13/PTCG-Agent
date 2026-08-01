
def register_rng_decomposition(aten_op):
    return decomp.register_decomposition(aten_op, rng_decompositions)

