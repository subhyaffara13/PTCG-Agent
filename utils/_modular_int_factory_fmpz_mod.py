
def _modular_int_factory_fmpz_mod(mod):
    index = operator.index
    fctx = flint.fmpz_mod_ctx(mod)
    fctx_poly = flint.fmpz_mod_poly_ctx(mod)
    fmpz_mod_poly = flint.fmpz_mod_poly

    def ctx(x):
        try:
            return fctx(x)
        except TypeError:
            # x might be Integer
            return fctx(index(x))

    def poly_ctx(cs):
        return fmpz_mod_poly(cs, fctx_poly)

    return ctx, poly_ctx

