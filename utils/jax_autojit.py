
def jax_autojit(
    func: Callable[P, T],
) -> Callable[P, T]:  # numpydoc ignore=PR01,RT01,SS03
    """
    Wrap `func` with ``jax.jit``, with the following differences:

    - Python scalar arguments and return values are not automatically converted to
      ``jax.Array`` objects.
    - All non-array arguments are automatically treated as static.
      Unlike ``jax.jit``, static arguments must be either hashable or serializable with
      ``pickle``.
    - Unlike ``jax.jit``, non-array arguments and return values are not limited to
      tuple/list/dict, but can be any object serializable with ``pickle``.
    - Automatically descend into non-array arguments and find ``jax.Array`` objects
      inside them, then rebuild the arguments when entering `func`, swapping the JAX
      concrete arrays with tracer objects.
    - Automatically descend into non-array return values and find ``jax.Array`` objects
      inside them, then rebuild them downstream of exiting the JIT, swapping the JAX
      tracer objects with concrete arrays.
    - Returned iterators are immediately completely consumed.

    See Also
    --------
    jax.jit : JAX JIT compilation function.

    Notes
    -----
    These are useful choices *for testing purposes only*, which is how this function is
    intended to be used. The output of ``jax.jit`` is a C++ level callable, that
    directly dispatches to the compiled kernel after the initial call. In comparison,
    ``jax_autojit`` incurs a much higher dispatch time.

    Additionally, consider::

        def f(x: Array, y: float, plus: bool) -> Array:
            return x + y if plus else x - y

        j1 = jax.jit(f, static_argnames="plus")
        j2 = jax_autojit(f)

    In the above example, ``j2`` requires a lot less setup to be tested effectively than
    ``j1``, but on the flip side it means that it will be re-traced for every different
    value of ``y``, which likely makes it not fit for purpose in production.
    """
    import jax

    @jax.jit  # type: ignore[untyped-decorator]  # pyright: ignore[reportUntypedFunctionDecorator]
    def inner(  # numpydoc ignore=GL08
        wargs: _AutoJITWrapper[Any],
    ) -> _AutoJITWrapper[T]:
        args, kwargs = wargs.obj
        res = func(*args, **kwargs)  # pyright: ignore[reportCallIssue]
        return _AutoJITWrapper(res)

    @wraps(func)
    def outer(*args: P.args, **kwargs: P.kwargs) -> T:  # numpydoc ignore=GL08
        wargs = _AutoJITWrapper((args, kwargs))
        return inner(wargs).obj

    return outer

