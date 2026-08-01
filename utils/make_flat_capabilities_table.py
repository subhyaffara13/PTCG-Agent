
def make_flat_capabilities_table(
        modules: str | list[str],
        backend_type: str,
        /,
        *,
        capabilities_table: dict | None = None,
) -> list[dict[str, str | int]]:
    """Generate full table of array api capabilities across public functions.

    Parameters
    ----------
    modules : str | list[str]
        A string containing single SciPy module, (e.g `scipy.stats`, `scipy.fft`)
        or a list of such strings.

    backend_type : {'cpu', 'gpu', 'jit', 'lazy'}

    capabilities_table : dict | None
        Table in the form of `scipy._lib._array_api.xp_capabilities_table`.
        If None, uses `scipy._lib._array_api.xp_capabilities_table`.
        Default: None.

    Returns
    -------
    output : list[dict[str, str]]
        `output` is a table in dict format
        (keys corresponding to column names). The first column is "module".
        The other columns correspond to supported backends for the given
        `backend_type`, e.g. jax.numpy, torch, and dask on cpu.
         numpy is excluded because it should always be supported.
         See the helper function
        `_process_capabilities_table_entry` above).

    """
    if backend_type not in {"cpu", "gpu", "jit", "lazy"}:
        raise ValueError(f"Received unhandled backend type {backend_type}")

    if isinstance(modules, str):
        modules = [modules]

    if capabilities_table is None:
        capabilities_table = xp_capabilities_table

    output = []

    for module_name in modules:
        module = import_module(module_name)
        public_things = module.__all__
        for name in public_things:
            if name in ALIASES.get(module_name, {}):
                # Skip undocumented aliases that are kept
                # for backwards compatibility reasons.
                continue
            thing = getattr(module, name)
            if is_inherently_out_of_scope(thing):
                continue
            entry = capabilities_table.get(thing, None)
            capabilities = _process_capabilities_table_entry(entry)[backend_type]
            row: dict[str, Any] = {"module": module_name}
            row.update({"function": name})
            row.update(capabilities)
            output.append(row)
    return output

