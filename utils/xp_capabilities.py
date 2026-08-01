
def xp_capabilities(
    *,
    # Alternative capabilities table.
    # Used only for testing this decorator.
    capabilities_table=None,
    # Generate pytest.mark.skip/xfail_xp_backends.
    # See documentation in conftest.py.
    # lists of tuples [(module name, reason), ...]
    skip_backends=(), xfail_backends=(),
    cpu_only=False, np_only=False, reason=None,
    out_of_scope=False, exceptions=(),
    # lists of tuples [(module name, reason), ...]
    warnings=(),
    # xpx.testing.lazy_xp_function kwargs.
    # Refer to array-api-extra documentation.
    allow_dask_compute=False, jax_jit=True,
    # Extra note to inject into the docstring
    extra_note=None,
    # Dictionary mapping method names to dictionaries of method
    # specific capabilities for use when when xp_capabilities is
    # applied to a class with varying capabilities per method
    method_capabilities=None,
    # Whether the function supports MArrays that wrap one of the supported backends
    marray=False,
):
    """Decorator for a function that states its support among various
    Array API compatible backends.

    This decorator has two effects:
    1. It allows tagging tests with ``@make_xp_test_case`` or
       ``make_xp_pytest_param`` (see below) to automatically generate
       SKIP/XFAIL markers and perform additional backend-specific
       testing, such as extra validation for Dask and JAX;
    2. It automatically adds a note to the function's docstring, containing
       a table matching what has been tested.

    See Also
    --------
    make_xp_test_case
    make_xp_pytest_param
    array_api_extra.testing.lazy_xp_function
    """
    capabilities_table = (xp_capabilities_table if capabilities_table is None
                          else capabilities_table)

    if out_of_scope:
        np_only = True

    if method_capabilities is None:
        method_capabilities = {}
    for method, capabilities in method_capabilities.items():
        # Fill in missing entries of method capabilities with
        # defaults if any entries are missing.
        method_capabilities[method] = dict(
            skip_backends=(),
            xfail_backends=(),
            cpu_only=False,
            np_only=False,
            out_of_scope=False,
            reason=None,
            exceptions=(),
            warnings=(),
            allow_dask_compute=False,
            jax_jit=True,
            marray=False,
        ) | capabilities

    capabilities = dict(
        skip_backends=skip_backends,
        xfail_backends=xfail_backends,
        cpu_only=cpu_only,
        np_only=np_only,
        out_of_scope=out_of_scope,
        reason=reason,
        exceptions=exceptions,
        allow_dask_compute=allow_dask_compute,
        jax_jit=jax_jit,
        warnings=warnings,
        method_capabilities=method_capabilities,
        marray=marray,
    )
    sphinx_capabilities = _make_sphinx_capabilities(**capabilities)

    def decorator(f):
        # Don't use a wrapper, as in some cases @xp_capabilities is
        # applied to a ufunc
        capabilities_table[f] = capabilities
        doc = FunctionDoc(f)
        if not np_only or out_of_scope:
            note = _make_capabilities_note(f.__name__, sphinx_capabilities, extra_note)
            doc['Notes'].append(note)
        doc = str(doc).split("\n", 1)[1].lstrip(" \n")  # remove signature
        try:
            f.__doc__ = doc
        except AttributeError:
            # Can't update __doc__ on ufuncs if SciPy
            # was compiled against NumPy < 2.2.
            pass

        return f
    return decorator

