
def make_xp_pytest_marks(*funcs, capabilities_table=None):
    """Variant of ``make_xp_test_case`` that returns a list of pytest marks,
    which can be used with the module-level `pytestmark = ...` variable::

        pytestmark = make_xp_pytest_marks(f1, f2)

        def test(xp):
            ...

    In this example, the whole test module is dedicated to testing `f1` or `f2`,
    and the two functions have the same capabilities, so it's unnecessary to
    cherry-pick which test tests which function.
    The above is equivalent to::

        pytestmark = [
            pytest.mark.skip_xp_backends(...),
            pytest.mark.xfail_xp_backends(...), ...]),
        ]

        def test(xp):
            ...

    See Also
    --------
    xp_capabilities
    make_xp_test_case
    make_xp_pytest_param
    array_api_extra.testing.lazy_xp_function
    """
    capabilities_table = (xp_capabilities_table if capabilities_table is None
                          else capabilities_table)
    import pytest

    marks = []
    # func may be a (cls, method_name) pair. This objs list will store cls
    # if the corresponding entry of funcs is such a tuple, and func otherwise.
    # the objs list is passed to the uses_xp_capabilities mark and used in
    # check_xp_untested. The intention is that all classes ``cls`` which advertise
    # support must have at least one test that uses the ``xp`` fixture along
    # with ``make_xp_test_case(cls)``. Testing is not enforced at the method level
    # since the documentation of capabilities is done at the class level.
    objs = []

    for func in funcs:
        if isinstance(func, tuple):
            cls, method = func
            capabilities = capabilities_table[cls]
            if method in capabilities["method_capabilities"]:
                capabilities = capabilities["method_capabilities"][method]
            objs.append(cls)
        else:
            capabilities = capabilities_table[func]
            objs.append(func)

        exceptions = capabilities['exceptions']
        reason = capabilities['reason']

        if capabilities['cpu_only']:
            marks.append(pytest.mark.skip_xp_backends(
                cpu_only=True, exceptions=exceptions, reason=reason))
        if capabilities['np_only']:
            marks.append(pytest.mark.skip_xp_backends(
                np_only=True, exceptions=exceptions, reason=reason))

        for mod_name, reason in capabilities['skip_backends']:
            marks.append(pytest.mark.skip_xp_backends(mod_name, reason=reason))
        for mod_name, reason in capabilities['xfail_backends']:
            marks.append(pytest.mark.xfail_xp_backends(mod_name, reason=reason))

        lazy_kwargs = {k: capabilities[k]
                       for k in ('allow_dask_compute', 'jax_jit')}
        lazy_xp_function(func, **lazy_kwargs)

    # Inject a marker which will help us identify tests using the xp
    # fixture which do not use xp_capabilities.
    marks.append(pytest.mark.uses_xp_capabilities(True, funcs=objs))

    return marks

