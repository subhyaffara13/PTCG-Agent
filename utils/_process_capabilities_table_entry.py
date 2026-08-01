
def _process_capabilities_table_entry(
    entry: dict | None
) -> dict[str, dict[str, BackendSupportStatus]]:
    """Returns dict showing alternative backend support in easy to consume form.

    Parameters
    ----------
    entry : dict | None
       A dict with the structure of the values of the dict
       scipy._lib._array_api.xp_capabilities_table. If None, it is
       assumped that no alternative backends are supported.
       Default: None.

    Returns
    -------
    dict[str, dict[str, bool]]
        The output dict currently has keys "cpu", "gpu", "jit" and "lazy".
        The value associated to each key is itself a dict. The keys of
        the inner dicts correspond to backends, with bool values stating
        whether or not the backend is supported with a given device or
        mode. Inapplicable backends do not appear in the inner dicts
        (e.g. since cupy is gpu-only, it does not appear in the inner
        dict keyed on "cpu"). Only alternative backends to NumPy are
        included since NumPY support should be guaranteed.

    """
    # This is a template for the output format. If more backends and
    # backend options are added, it will need to be updated manually.
    # Entries start as boolean, but upon returning, will take values
    # from the BackendSupportStatus Enum.
    output = {
        "cpu": {"torch": False, "jax": False, "dask": False},
        "gpu": {"cupy": False, "torch": False, "jax": False},
        "jit": {"jax": False},
        "lazy": {"dask": False},
    }
    S = BackendSupportStatus
    if entry is None:
        # If there is no entry, assume no alternative backends are supported.
        # If the list of supported backends will grows, this hard-coded dict
        # will need to be updated.
        return {
            outer_key: {inner_key: S.UNKNOWN for inner_key in outer_value}
            for outer_key, outer_value in output.items()
        }

    if entry["out_of_scope"]:
        # None is used to signify out-of-scope functions.
        return {
            outer_key: {inner_key: S.OUT_OF_SCOPE for inner_key in outer_value}
            for outer_key, outer_value in output.items()
        }

    # For now, use _make_sphinx_capabilities because that's where
    # the relevant logic for determining what is and isn't
    # supported based on xp_capabilities_table entries lives.
    # This logic should be decoupled from this function due to exceptions; e.g. marray.
    sphinx_capabilities = _make_sphinx_capabilities(**entry)
    sphinx_capabilities.pop("marray")
    for backend, capabilities in sphinx_capabilities.items():
        if backend in {"array_api_strict", "numpy"}:
            continue
        backend = BACKEND_NAMES_MAP.get(backend, backend)
        cpu, gpu = capabilities.cpu, capabilities.gpu
        if cpu is not None:
            if backend not in output["cpu"]:
                raise ValueError(
                    "Input capabilities table entry contains unhandled"
                    f" backend {backend} on cpu."
                )
            output["cpu"][backend] = cpu
        if gpu is not None:
            if backend not in output["gpu"]:
                raise ValueError(
                    "Input capabilities table entry contains unhandled"
                    f" backend {backend} on gpu."
                )
            output["gpu"][backend] = gpu
        if backend == "jax":
            output["jit"]["jax"] = entry["jax_jit"] and output["cpu"]["jax"]
        if backend == "dask.array":
            support_lazy = not entry["allow_dask_compute"] and output["dask"]
            output["lazy"]["dask"] = bool(support_lazy)
    return {
        outer_key: {
            inner_key: S.YES if inner_value else S.NO
            for inner_key, inner_value in outer_value.items()
        }
        for outer_key, outer_value in output.items()
    }

