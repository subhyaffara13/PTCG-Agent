
def parametrize_blas(func_name, prefixes, modules=None):
    """Parametrize a test over BLAS prefixes, "sdcz", and over the BLAS modules,
    `fblas,fblas_64.

    Given a func_name "gemm", this generates a pytest parametrization over up to 8
    variants: sgemm, dgemm, cgemm, zgemm, each loaded from `fblas` (i.e. 32-bit LP64
    variants) and `fblas_64` (i.e. 64-bit ILP64 variants)..

    If a module is not available, the pytest parameter has a skip mark, so that the
    test is skipped with a descriptive message.

    Parameters
    ----------
    func_name : str
        The base name of a BLAS function, e.g. "gemm"
    prefixes : str or sequence
        BLAS prefixes to prepend to `func_name`.
        E.g. ``func_name='gemm', prefixes='cz'`` generates `cgemm` and `zgemm`.
    modules : sequence of ``(module, str)`` pairs
        BLAS modules to fetch functions from. By default, use `fblas` (LP64 variant)
        and fblas_64 (ILP64 variant).
    """
    if modules is None:
        modules = [(fblas, "fblas"), (fblas_64, "fblas_64")]

    params = []
    for mod, mod_name in modules:
        for prefix in prefixes:
            dtype = _dt_from_prefix(prefix)
            if mod is None:
                param_ = pytest.param(
                    None, dtype,
                    id=f"{mod_name}.{prefix}{func_name}",
                    marks=pytest.mark.skip(reason=f"{mod_name} is not available")
                )
            else:
                # Fetch the BLAS function from the BLAS module. NB: if the name is not
                # found in the module, it's a hard failure (all names must be present).
                f = getattr(mod, prefix + func_name)
                param_ = pytest.param(f, dtype, id=f"{mod_name}.{prefix}{func_name}")

            params.append(param_)

    return pytest.mark.parametrize("f, dtype", params)

