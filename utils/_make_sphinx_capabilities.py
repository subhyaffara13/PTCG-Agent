
def _make_sphinx_capabilities(
    # lists of tuples [(module name, reason), ...]
    skip_backends=(), xfail_backends=(),
    # @pytest.mark.skip/xfail_xp_backends kwargs
    cpu_only=False, np_only=False, out_of_scope=False, exceptions=(),
    # xpx.lazy_xp_backends kwargs
    allow_dask_compute=False, jax_jit=True,
    # list of tuples [(module name, reason), ...]
    warnings = (),
    # Whether the function supports MArrays that wrap one of the supported backends
    marray=None,
    # unused in documentation
    reason=None,
    method_capabilities=None,
):
    if out_of_scope:
        return {"out_of_scope": True}

    exceptions = set(exceptions)

    # Default capabilities
    capabilities = {
        "numpy": _XPSphinxCapability(cpu=True, gpu=None),
        "array_api_strict": _XPSphinxCapability(cpu=True, gpu=None),
        "cupy": _XPSphinxCapability(cpu=None, gpu=True),
        "torch": _XPSphinxCapability(cpu=True, gpu=True),
        "jax.numpy": _XPSphinxCapability(cpu=True, gpu=True,
            warnings=[] if jax_jit else ["no JIT"]),
        # Note: Dask+CuPy is currently untested and unsupported
        "dask.array": _XPSphinxCapability(cpu=True, gpu=None,
            warnings=["computes graph"] if allow_dask_compute else []),
    }

    # documentation doesn't display the reason
    for module, _ in list(skip_backends) + list(xfail_backends):
        backend = capabilities[module]
        if backend.cpu is not None:
            backend.cpu = False
        if backend.gpu is not None:
            backend.gpu = False

    for module, backend in capabilities.items():
        if np_only and module not in exceptions | {"numpy"}:
            if backend.cpu is not None:
                backend.cpu = False
            if backend.gpu is not None:
                backend.gpu = False
        elif cpu_only and module not in exceptions and backend.gpu is not None:
            backend.gpu = False

    for module, warning in warnings:
        backend = capabilities[module]
        backend.warnings.append(warning)

    # MArrays are either supported or not. If supported, they work with all combinations
    # of device + backend that are supported by the function and MArray itself. This is
    # indicated with an extra note after the backend table.
    capabilities.update({'marray': marray})

    return capabilities

