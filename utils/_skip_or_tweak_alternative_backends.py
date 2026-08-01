
def _skip_or_tweak_alternative_backends(xp, nfo, dtypes, int_only):
    """Skip tests for specific intersections of scipy.special functions 
    vs. backends vs. dtypes vs. devices.
    Also suggest bespoke tweaks.

    Returns
    -------
    positive_only : list[bool]
        Whether you should exclusively test positive inputs.
    dtypes : list[str]
        dtype strings 'float64', 'int32', 'int64', etc. with integer types
        mapped to the type of the NumPy default int.
    """
    f_name = nfo.name
    if isinstance(nfo.positive_only, dict):
        positive_only = nfo.positive_only.get(get_native_namespace_name(xp), False)
    else:
        positive_only = nfo.positive_only
    if isinstance(positive_only, bool):
        positive_only = [positive_only]*nfo.n_args

    dtypes = [np.intp.__name__ if dtype == "intp" else dtype for dtype in dtypes]

    if f_name in {'betaincinv'} and is_cupy(xp):
        pytest.xfail("CuPy uses different convention for out of domain input.")

    if not any('int' in dtype for dtype in dtypes):
        return positive_only, dtypes

    # Integer-specific issues from this point onwards

    if f_name in {'gamma', 'gammasgn'} and is_cupy(xp):
        # CuPy has not yet updated gamma pole behavior to match
        # https://github.com/scipy/scipy/pull/21827.
        positive_only = [True]

    if f_name in {'poch'} and is_jax(xp):
        # Jax uses a different convention at gamma poles.
        positive_only = [True, True]

    if f_name == 'multigammaln':
        pytest.skip("multigammaln raises for out of domain inputs.")

    if ((is_torch(xp) and f_name in {'gammainc', 'gammaincc'})
        or (is_cupy(xp) and f_name in {'stdtr', 'i0e', 'i1e'})
        or (is_jax(xp) and f_name in {'stdtr', 'ndtr', 'ndtri', 'log_ndtr', 'hyp1f1',
                                      'hyp2f1', 'spence', 'kl_div'})
    ):
        pytest.skip(f"`{f_name}` does not support integer types")

    # int/float mismatched args support is sketchy
    if (any('float' in dtype for dtype in dtypes)
        and ((is_torch(xp) and f_name in ('rel_entr', 'xlogy', 'polygamma',
                                          'zeta', 'xlog1py'))
             or (is_jax(xp) and f_name in ('gammainc', 'gammaincc', 'expn',
                                           'rel_entr', 'xlogy', 'betaln',
                                           'polygamma', 'zeta', 'poch',
                                           'xlog1py')))
    ):
        pytest.xfail("dtypes do not match")

    if (is_torch(xp) and xpx.default_dtype(xp) == xp.float32):
        # On PyTorch with float32 default dtype, all ints are promoted
        # to float32, but when falling back to NumPy/SciPy int64 is promoted
        # instead to float64. Integer only parameters essentially do not
        # participate in determination of the result type in PyTorch with
        # float32 default dtype, but will impact the output dtype as if
        # they were float64 when falling back to NumPy/SciPy.
        if not nfo.torch_native:
            pytest.xfail("dtypes do not match")

    return positive_only, dtypes

