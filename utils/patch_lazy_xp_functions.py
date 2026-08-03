from typing import Any, Callable

def patch_lazy_xp_functions(
    request: pytest.FixtureRequest,
    monkeypatch: pytest.MonkeyPatch | None = None,
    *,
    xp: ModuleType,
) -> contextlib.AbstractContextManager[None]:
    """
    Test lazy execution of functions tagged with :func:`lazy_xp_function`.

    If ``xp==jax.numpy``, search for all functions and methods which have been tagged
    with :func:`lazy_xp_function` in the globals of the module that defines the current
    test, as well as in the ``lazy_xp_modules`` list in the globals of the same module,
    and wrap them with :func:`jax.jit`.
    Unwrap them at the end of the test.

    If ``xp==dask.array``, wrap the functions with a decorator that disables
    ``compute()`` and ``persist()`` and ensures that exceptions and warnings are raised
    eagerly.

    This function should be typically called by your library's `xp` fixture that runs
    tests on multiple backends::

        @pytest.fixture(params=[
            numpy,
            array_api_strict,
            pytest.param(jax.numpy, marks=pytest.mark.thread_unsafe),
            pytest.param(dask.array, marks=pytest.mark.thread_unsafe),
        ])
        def xp(request):
            with patch_lazy_xp_functions(request, xp=request.param):
                yield request.param

    but it can be otherwise be called by the test itself too.

    Parameters
    ----------
    request : pytest.FixtureRequest
        Pytest fixture, as acquired by the test itself or by one of its fixtures.
    monkeypatch : pytest.MonkeyPatch
        Deprecated
    xp : array_namespace
        Array namespace to be tested.

    See Also
    --------
    lazy_xp_function : Tag a function to be tested on lazy backends.
    pytest.FixtureRequest : `request` test function parameter.

    Notes
    -----
    This context manager monkey-patches modules and as such is thread unsafe
    on Dask and JAX. If you run your test suite with
    `pytest-run-parallel <https://github.com/Quansight-Labs/pytest-run-parallel/>`_,
    you should mark these backends with ``@pytest.mark.thread_unsafe``, as shown in
    the example above.
    """
    mod = cast(ModuleType, request.module)
    search_targets: list[ModuleType | type] = [
        mod,
        *cast(list[ModuleType], getattr(mod, "lazy_xp_modules", [])),
    ]
    # Also search for classes within the above modules which have had lazy_xp_function
    # applied to methods through ``lazy_xp_function((cls, method_name))`` syntax.
    # We might end up adding classes incidentally imported into modules, so using a
    # set here to cut down on potential redundancy.
    classes: set[type] = set()
    for target in search_targets:
        for obj in target.__dict__.values():
            if isinstance(obj, type):
                classes.add(obj)
    search_targets.extend(classes)

    to_revert: list[tuple[ModuleType | type, str, object]] = []

    def temp_setattr(target: ModuleType | type, name: str, func: object) -> None:
        """
        Variant of monkeypatch.setattr, which allows monkey-patching only selected
        parameters of a test so that pytest-run-parallel can run on the remainder.
        """
        assert hasattr(target, name)
        # Need getattr_static because the attr could be a staticmethod or other
        # descriptor and we don't want that to be stripped away.
        original = getattr_static(target, name)
        to_revert.append((target, name, original))
        setattr(target, name, func)

    if monkeypatch is not None:
        warnings.warn(
            (
                "The `monkeypatch` parameter is deprecated and will be removed in a "
                "future version. "
                "Use `patch_lazy_xp_function` as a context manager instead."
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        # Enable using patch_lazy_xp_function not as a context manager
        temp_setattr = monkeypatch.setattr  # type: ignore[assignment]  # pyright: ignore[reportAssignmentType]

    def iter_tagged() -> Iterator[
        tuple[ModuleType | type, str, Any, Callable[..., Any], dict[str, Any]]
    ]:
        for target in search_targets:
            for name, attr in target.__dict__.items():
                # attr might be a staticmethod or classmethod. If so we need
                # to peel it back and wrap the underlying function and later
                # make sure not to accidentally replace it with a regular
                # method.
                func: Any = (
                    attr.__func__
                    if isinstance(attr, (staticmethod, classmethod))
                    else attr
                )
                tags: dict[str, Any] | None = None
                with contextlib.suppress(AttributeError):
                    tags = func._lazy_xp_function  # pylint: disable=protected-access
                if tags is None:
                    with contextlib.suppress(KeyError, TypeError):
                        tags = _ufuncs_tags[func]
                if tags is not None:
                    if isinstance(target, type) and tags.get("owner") is not target:
                        # There's a common pattern to wrap functions in namespace
                        # classes to bypass lazy_xp_function like this:
                        #
                        # class naked:
                        #     myfunc = mymodule.myfunc
                        #
                        # To ensure this still works when checking for tags in
                        # attributes of classes, ensure that target is the actual
                        # owning class where func was defined.
                        continue
                    # put attr, and func in the outputs so we can later tell
                    # if this was a staticmethod or classmethod.
                    yield target, name, attr, func, tags

    wrapped: Any
    if is_dask_namespace(xp):
        for target, name, attr, func, tags in iter_tagged():
            n = tags["allow_dask_compute"]
            if n is True:
                n = 1_000_000
            elif n is False:
                n = 0
            wrapped = _dask_wrap(func, n)
            # If we're dealing with a staticmethod or classmethod, make
            # sure things stay that way.
            if isinstance(attr, staticmethod):
                wrapped = staticmethod(wrapped)
            elif isinstance(attr, classmethod):
                wrapped = classmethod(wrapped)
            temp_setattr(target, name, wrapped)

    elif is_jax_namespace(xp):
        for target, name, attr, func, tags in iter_tagged():
            if tags["jax_jit"]:
                wrapped = jax_autojit(func)
                # If we're dealing with a staticmethod or classmethod, make
                # sure things stay that way.
                if isinstance(attr, staticmethod):
                    wrapped = staticmethod(wrapped)
                elif isinstance(attr, classmethod):
                    wrapped = classmethod(wrapped)
                temp_setattr(target, name, wrapped)

    # We can't just decorate patch_lazy_xp_functions with
    # @contextlib.contextmanager because it would not work with the
    # deprecated monkeypatch when not used as a context manager.
    @contextlib.contextmanager
    def revert_on_exit() -> Generator[None]:
        try:
            yield
        finally:
            for target, name, orig_func in to_revert:
                setattr(target, name, orig_func)

    return revert_on_exit()

