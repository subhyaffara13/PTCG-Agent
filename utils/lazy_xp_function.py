from typing import Any, Callable

def lazy_xp_function(
    func: Callable[..., Any] | tuple[type, str],
    *,
    allow_dask_compute: bool | int = False,
    jax_jit: bool = True,
    static_argnums: Deprecated = DEPRECATED,
    static_argnames: Deprecated = DEPRECATED,
) -> None:  # numpydoc ignore=GL07
    """
    Tag a function to be tested on lazy backends.

    Tag a function so that when any tests are executed with ``xp=jax.numpy`` the
    function is replaced with a jitted version of itself, and when it is executed with
    ``xp=dask.array`` the function will raise if it attempts to materialize the graph.
    This will be later expanded to provide test coverage for other lazy backends.

    In order for the tag to be effective, the test or a fixture must call
    :func:`patch_lazy_xp_functions`.

    Parameters
    ----------
    func : callable | tuple[type, str]
        Function to be tested, or a tuple containing an (uninstantiated) class and a
        method name to specify a class method to be tested.
    allow_dask_compute : bool | int, optional
        Whether `func` is allowed to internally materialize the Dask graph, or maximum
        number of times it is allowed to do so. This is typically triggered by
        ``bool()``, ``float()``, or ``np.asarray()``.

        Set to 1 if you are aware that `func` converts the input parameters to NumPy and
        want to let it do so at least for the time being, knowing that it is going to be
        extremely detrimental for performance.

        If a test needs values higher than 1 to pass, it is a canary that the conversion
        to NumPy/bool/float is happening multiple times, which translates to multiple
        computations of the whole graph. Short of making the function fully lazy, you
        should at least add explicit calls to ``np.asarray()`` early in the function.
        *Note:* the counter of `allow_dask_compute` resets after each call to `func`, so
        a test function that invokes `func` multiple times should still work with this
        parameter set to 1.

        Set to True to allow `func` to materialize the graph an unlimited number
        of times.

        Default: False, meaning that `func` must be fully lazy and never materialize the
        graph.
    jax_jit : bool, optional
        Set to True to replace `func` with a smart variant of ``jax.jit(func)`` after
        calling the :func:`patch_lazy_xp_functions` test helper with ``xp=jax.numpy``.
        This is the default behaviour.
        Set to False if `func` is only compatible with eager (non-jitted) JAX.

        Unlike with vanilla ``jax.jit``, all arguments and return types that are not JAX
        arrays are treated as static; the function can accept and return arbitrary
        wrappers around JAX arrays. This difference is because, in real life, most users
        won't wrap the function directly with ``jax.jit`` but rather they will use it
        within their own code, which is itself then wrapped by ``jax.jit``, and
        internally consume the function's outputs.

        In other words, the pattern that is being tested is::

            >>> @jax.jit
            ... def user_func(x):
            ...     y = user_prepares_inputs(x)
            ...     z = func(y, some_static_arg=True)
            ...     return user_consumes(z)

        Default: True.
    static_argnums :
        Deprecated; ignored
    static_argnames :
        Deprecated; ignored

    See Also
    --------
    patch_lazy_xp_functions : Companion function to call from the test or fixture.
    jax.jit : JAX function to compile a function for performance.

    Examples
    --------
    In ``test_mymodule.py``::

      from array_api_extra.testing import lazy_xp_function from mymodule import myfunc

      lazy_xp_function(myfunc)

      def test_myfunc(xp):
          a = xp.asarray([1, 2])
          # When xp=jax.numpy, this is similar to `b = jax.jit(myfunc)(a)`
          # When xp=dask.array, crash on compute() or persist()
          b = myfunc(a)

    Notes
    -----
    In order for this tag to be effective, the test function must be imported into the
    test module globals without its namespace; alternatively its namespace must be
    declared in a ``lazy_xp_modules`` list in the test module globals.

    Example 1::

      from mymodule import myfunc

      lazy_xp_function(myfunc)

      def test_myfunc(xp):
          x = myfunc(xp.asarray([1, 2]))

    Example 2::

      import mymodule

      lazy_xp_modules = [mymodule]
      lazy_xp_function(mymodule.myfunc)

      def test_myfunc(xp):
          x = mymodule.myfunc(xp.asarray([1, 2]))

    A test function can circumvent this monkey-patching system by using a namespace
    outside of the two above patterns. You need to sanitize your code to make sure this
    only happens intentionally.

    Example 1::

      import mymodule
      from mymodule import myfunc

      lazy_xp_function(myfunc)

      def test_myfunc(xp):
          a = xp.asarray([1, 2])
          b = myfunc(a)  # This is wrapped when xp=jax.numpy or xp=dask.array
          c = mymodule.myfunc(a)  # This is not

    Example 2::

      import mymodule

      class naked:
          myfunc = mymodule.myfunc

      lazy_xp_modules = [mymodule]
      lazy_xp_function(mymodule.myfunc)

      def test_myfunc(xp):
          a = xp.asarray([1, 2])
          b = mymodule.myfunc(a)  # This is wrapped when xp=jax.numpy or xp=dask.array
          c = naked.myfunc(a)  # This is not
    """
    if static_argnums is not DEPRECATED or static_argnames is not DEPRECATED:
        warnings.warn(
            (
                "The `static_argnums` and `static_argnames` parameters are deprecated "
                "and ignored. They will be removed in a future version."
            ),
            DeprecationWarning,
            stacklevel=2,
        )
    tags: dict[str, bool | int | type] = {
        "allow_dask_compute": allow_dask_compute,
        "jax_jit": jax_jit,
    }

    if isinstance(func, tuple):
        # Replace the method with a clone before adding tags
        # to avoid adding unwanted tags to a parent method when
        # the method was inherited from a parent class.
        # Note: can't just accept an unbound method `cls.method_name` because in
        # case of inheritance it would be impossible to attribute it to the child class.
        # This also makes it so tagged methods will appear in their class's ``__dict__``
        # and thus findable by ``iter_tagged_modules`` below.
        cls, method_name = func
        # The method might be a staticmethod or classmethod so we need to do a dance
        # to ensure that this is preserved.
        raw_attr = getattr_static(cls, method_name)
        method = getattr(cls, method_name)
        if isinstance(raw_attr, classmethod):
            method = method.__func__
        cloned_method = _clone_function(method)

        method_to_set: Any
        if isinstance(raw_attr, staticmethod):
            method_to_set = staticmethod(cloned_method)
        elif isinstance(raw_attr, classmethod):
            method_to_set = classmethod(cloned_method)
        else:
            method_to_set = cloned_method

        setattr(cls, method_name, method_to_set)
        f = getattr(cls, method_name)
        if isinstance(raw_attr, classmethod):
            f = f.__func__
        # Annotate that cls owns this method so we can check that later.
        tags["owner"] = cls
    else:
        f = func

    try:
        f._lazy_xp_function = tags  # pylint: disable=protected-access  # pyright: ignore[reportFunctionMemberAccess]
    except AttributeError:  # @cython.vectorize
        _ufuncs_tags[f] = tags

