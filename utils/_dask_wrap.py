
def _dask_wrap(
    func: Callable[P, T], n: int
) -> Callable[P, T]:  # numpydoc ignore=PR01,RT01
    """
    Wrap `func` to raise if it attempts to call `dask.compute` more than `n` times.

    After the function returns, materialize the graph in order to re-raise exceptions.
    """
    import dask
    import dask.array as da

    func_name = getattr(func, "__name__", str(func))
    n_str = f"only up to {n}" if n else "no"
    msg = (
        f"Called `dask.compute()` or `dask.persist()` {n + 1} times, "
        f"but {n_str} calls are allowed. Set "
        f"`lazy_xp_function({func_name}, allow_dask_compute={n + 1})` "
        "to allow for more (but note that this will harm performance). "
    )

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:  # numpydoc ignore=GL08
        scheduler = CountingDaskScheduler(n, msg)
        with dask.config.set({"scheduler": scheduler}):  # pyright: ignore[reportPrivateImportUsage]
            out = func(*args, **kwargs)

        # Block until the graph materializes and reraise exceptions. This allows
        # `pytest.raises` and `pytest.warns` to work as expected. Note that this would
        # not work on scheduler='distributed', as it would not block.
        arrays, rest = pickle_flatten(out, da.Array)
        arrays = dask.persist(arrays, scheduler="threads")[0]  # type: ignore[attr-defined,no-untyped-call]  # pyright: ignore[reportPrivateImportUsage]
        return pickle_unflatten(arrays, rest)  # pyright: ignore[reportUnknownArgumentType]

    return wrapper

