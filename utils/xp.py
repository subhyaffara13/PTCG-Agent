
def xp(request):
    """Run the test that uses this fixture on each available array API library.

    You can select all and only the tests that use the `xp` fixture by
    passing `-m array_api_backends` to pytest.

    You can select where individual tests run through the `@skip_xp_backends`,
    `@xfail_xp_backends`, and `@skip_xp_invalid_arg` pytest markers.

    Please read: https://docs.scipy.org/doc/scipy/dev/api-dev/array_api.html#adding-tests
    """
    # Read all @pytest.marks.skip_xp_backends markers that decorate to the test,
    # if any, and raise pytest.skip() if the current xp is in the list.
    skip_or_xfail_xp_backends(request, "skip")
    # Read all @pytest.marks.xfail_xp_backends markers that decorate the test,
    # if any, and raise pytest.xfail() if the current xp is in the list.
    skip_or_xfail_xp_backends(request, "xfail")

    # Check if ``uses_xp_capabilities`` mark is present.
    # ``scipy._lib._array_api.make_xp_pytest_marks``, which draws from
    # ``xp_capabilities``, will set ``pytest.mark.uses_xp_capabilities(True)``.
    # Tests which are unconverted or which are for private functions without
    # ``xp_capabilities`` entries should have
    # ``pytest.mark.uses_xp_capabilities(False)`` explicitly set.
    if request.node.get_closest_marker("uses_xp_capabilities") is None:
        warnings.warn(
            "test uses `xp` fixture without drawing from `xp_capabilities` "
            " but is not explicitly marked with"
            " ``pytest.mark.uses_xp_capabilities(False)``",
            stacklevel=0,
        )

    xp = request.param
    # Potentially wrap namespace with array_api_compat
    xp = array_namespace(xp.empty(0))

    if SCIPY_ARRAY_API:
        # If xp==jax.numpy, wrap tested functions in jax.jit
        # If xp==dask.array, wrap tested functions to test that graph is not computed
        with patch_lazy_xp_functions(request=request, xp=request.param):
            # Throughout all calls to assert_almost_equal, assert_array_almost_equal,
            # and xp_assert_* functions, test that the array namespace is xp in both
            # the expected and actual arrays. This is to detect the case where both
            # arrays are erroneously just plain numpy while xp is something else.
            with default_xp(xp):
                yield xp
    else:
        yield xp

