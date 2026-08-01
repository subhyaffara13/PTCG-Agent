
def _modular_int_factory(mod, dom, symmetric, self):
    # Convert the modulus to ZZ
    try:
        mod = dom.convert(mod)
    except CoercionFailed:
        raise ValueError('modulus must be an integer, got %s' % mod)

    ctx, poly_ctx, is_flint = None, None, False

    # Don't use flint if the modulus is not prime as it often crashes.
    if flint is not None and mod.is_prime():

        is_flint = True

        # Try to use flint's nmod first
        ctx, poly_ctx = _modular_int_factory_nmod(mod)

        if ctx is None:
            # Use fmpz_mod for larger moduli
            ctx, poly_ctx = _modular_int_factory_fmpz_mod(mod)

    if ctx is None:
        # Use the Python implementation if flint is not available or the
        # modulus is not prime.
        ctx = ModularIntegerFactory(mod, dom, symmetric, self)
        poly_ctx = None  # not used

    return ctx, poly_ctx, is_flint

