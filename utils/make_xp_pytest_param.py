
def make_xp_pytest_param(func, *args, additional_marks=None, capabilities_table=None):
    """Variant of ``make_xp_test_case`` that returns a pytest.param for a function,
    with all necessary skip_xp_backends and xfail_xp_backends marks applied::

        @pytest.mark.parametrize(
            "func", [make_xp_pytest_param(f1), make_xp_pytest_param(f2)]
        )
        def test(func, xp):
            ...

    The above is equivalent to::

        @pytest.mark.parametrize(
            "func", [
                pytest.param(f1, marks=[
                    pytest.mark.skip_xp_backends(...),
                    pytest.mark.xfail_xp_backends(...), ...]),
                pytest.param(f2, marks=[
                    pytest.mark.skip_xp_backends(...),
                    pytest.mark.xfail_xp_backends(...), ...]),
        )
        def test(func, xp):
            ...

    Parameters
    ----------
    func : Callable | tuple[type, str]
        Function to be tested. It must be decorated with ``@xp_capabilities``.
        Alternatively, a tuple of the form ``(cls, method_name)``, where
        ``cls`` must be decorated with ``@xp_capabilities``, specifying
        that one wants marks for a particular method of the given class.
        See the Notes section of the docstring for ``make_xp_test_case`` for
        more info.

        Note that if func is a tuple, then only the first entry is actually
        used in the resulting pytest param, and the second entry is only
        used to specify capabilities for a particular given method and tell
        the testing infra to apply ``lazy_xp_function`` to that method.::

        @pytest.mark.parametrize("cls", [(A, "f"), (B, "f"), C])
        def test(cls, xp):
            # cls iterates over A, B, C.
    *args : Any, optional
        Extra pytest parameters for the use case, e.g.::

        @pytest.mark.parametrize("func,verb", [
            make_xp_pytest_param(f1, "hello"),
            make_xp_pytest_param(f2, "world")])
        def test(func, verb, xp):
            # iterates on (func=f1, verb="hello")
            # and (func=f2, verb="world")
    additional_marks : pytest.MarkDecorator | list[pytest.MarkDecorator]
        Additional pytest marks to add to the parameter, e.g.
        ``pytest.mark.slow``.

    See Also
    --------
    xp_capabilities
    make_xp_test_case
    make_xp_pytest_marks
    array_api_extra.testing.lazy_xp_function
    """
    import pytest

    marks = make_xp_pytest_marks(func, capabilities_table=capabilities_table)
    if additional_marks is not None:
        if isinstance(additional_marks, pytest.MarkDecorator):
            additional_marks = [additional_marks]
        marks.extend(additional_marks)
    if isinstance(func, tuple):
        func, _ = func
    return pytest.param(func, *args, marks=marks, id=func.__name__)

