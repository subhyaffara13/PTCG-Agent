
def is_lazy_array(x: object) -> TypeGuard[_ArrayApiObj]:
    """Return True if x is potentially a future or it may be otherwise impossible or
    expensive to eagerly read its contents, regardless of their size, e.g. by
    calling ``bool(x)`` or ``float(x)``.

    Return False otherwise; e.g. ``bool(x)`` etc. is guaranteed to succeed and to be
    cheap as long as the array has the right dtype and size.

    Note
    ----
    This function errs on the side of caution for array types that may or may not be
    lazy, e.g. JAX arrays, by always returning True for them.
    """
    # **JAX note:** while it is possible to determine if you're inside or outside
    # jax.jit by testing the subclass of a jax.Array object, as well as testing bool()
    # as we do below for unknown arrays, this is not recommended by JAX best practices.

    # **Dask note:** Dask eagerly computes the graph on __bool__, __float__, and so on.
    # This behaviour, while impossible to change without breaking backwards
    # compatibility, is highly detrimental to performance as the whole graph will end
    # up being computed multiple times.

    # Note: skipping reclassification of JAX zero gradient arrays, as one will
    # exclusively get them once they leave a jax.grad JIT context.
    cls = cast(Hashable, type(x))
    res = _is_lazy_cls(cls)
    if res is not None:
        return res

    if not hasattr(x, "__array_namespace__"):
        return False

    # Unknown Array API compatible object. Note that this test may have dire consequences
    # in terms of performance, e.g. for a lazy object that eagerly computes the graph
    # on __bool__ (dask is one such example, which however is special-cased above).

    # Select a single point of the array
    s = size(cast("HasShape[Collection[SupportsIndex | None]]", x))
    if s is None:
        return True
    xp = array_namespace(x)
    if s > 1:
        x = xp.reshape(x, (-1,))[0]
    # Cast to dtype=bool and deal with size 0 arrays
    x = xp.any(x)

    try:
        bool(x)
        return False
    # The Array API standard dictactes that __bool__ should raise TypeError if the
    # output cannot be defined.
    # Here we allow for it to raise arbitrary exceptions, e.g. like Dask does.
    except Exception:
        return True

