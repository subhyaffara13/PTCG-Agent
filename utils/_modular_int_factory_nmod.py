
def _modular_int_factory_nmod(mod):
    # nmod only recognises int
    index = operator.index
    mod = index(mod)
    nmod = flint.nmod
    nmod_poly = flint.nmod_poly

    # flint's nmod is only for moduli up to 2^64-1 (on a 64-bit machine)
    try:
        nmod(0, mod)
    except OverflowError:
        return None, None

    def ctx(x):
        try:
            return nmod(x, mod)
        except TypeError:
            return nmod(index(x), mod)

    def poly_ctx(cs):
        return nmod_poly(cs, mod)

    return ctx, poly_ctx

