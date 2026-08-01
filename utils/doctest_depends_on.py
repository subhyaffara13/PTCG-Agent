
def doctest_depends_on(exe=None, modules=None, disable_viewers=None,
                       python_version=None, ground_types=None):
    """
    Adds metadata about the dependencies which need to be met for doctesting
    the docstrings of the decorated objects.

    ``exe`` should be a list of executables

    ``modules`` should be a list of modules

    ``disable_viewers`` should be a list of viewers for :func:`~sympy.printing.preview.preview` to disable

    ``python_version`` should be the minimum Python version required, as a tuple
    (like ``(3, 0)``)
    """
    dependencies = {}
    if exe is not None:
        dependencies['executables'] = exe
    if modules is not None:
        dependencies['modules'] = modules
    if disable_viewers is not None:
        dependencies['disable_viewers'] = disable_viewers
    if python_version is not None:
        dependencies['python_version'] = python_version
    if ground_types is not None:
        dependencies['ground_types'] = ground_types

    def skiptests():
        from sympy.testing.runtests import DependencyError, SymPyDocTests, PyTestReporter # lazy import
        r = PyTestReporter()
        t = SymPyDocTests(r, None)
        try:
            t._check_dependencies(**dependencies)
        except DependencyError:
            return True  # Skip doctests
        else:
            return False # Run doctests

    def depends_on_deco(fn):
        fn._doctest_depends_on = dependencies
        fn.__doctest_skip__ = skiptests

        if inspect.isclass(fn):
            fn._doctest_depdends_on = no_attrs_in_subclass(
                fn, fn._doctest_depends_on)
            fn.__doctest_skip__ = no_attrs_in_subclass(
                fn, fn.__doctest_skip__)
        return fn

    return depends_on_deco

