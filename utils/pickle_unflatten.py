
def pickle_unflatten(instances: Iterable[object], rest: FlattenRest) -> Any:
    """
    Reverse of ``pickle_flatten``.

    Parameters
    ----------
    instances : Iterable
        Inner objects to be reinserted into the flattened container.
    rest : FlattenRest
        Extra bits, as returned by ``pickle_flatten``.

    Returns
    -------
    object
        The outer object originally passed to ``pickle_flatten`` after a
        pickle->unpickle round-trip.

    See Also
    --------
    pickle_flatten : Serializing function.
    pickle.loads : Standard unpickle function.

    Notes
    -----
    The `instances` iterable must yield at least the same number of elements as the ones
    returned by ``pickle_flatten``, but the elements do not need to be the same objects
    or even the same types of objects. Excess elements, if any, will be left untouched.
    """
    iters = iter(instances), iter(rest)
    pik = cast(bytes, next(iters[1]))

    class Unpickler(pickle.Unpickler):  # numpydoc ignore=GL08
        """Mirror of the overridden Pickler in pickle_flatten."""

        @override
        def persistent_load(self, pid: Literal[0, 1]) -> object:  # numpydoc ignore=GL08
            try:
                return next(iters[pid])
            except StopIteration as e:
                msg = "Not enough objects to unpickle"
                raise ValueError(msg) from e

    f = io.BytesIO(pik)
    return Unpickler(f).load()

