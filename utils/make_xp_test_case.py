
def make_xp_test_case(*funcs, capabilities_table=None):
    capabilities_table = (xp_capabilities_table if capabilities_table is None
                          else capabilities_table)
    """Generate pytest decorator for a test function that tests functionality
    of one or more Array API compatible functions.

    Read the parameters of the ``@xp_capabilities`` decorator applied to the
    listed functions and:

    - Generate the ``@pytest.mark.skip_xp_backends`` and
      ``@pytest.mark.xfail_xp_backends`` decorators
      for the decorated test function
    - Tag the function with `xpx.testing.lazy_xp_function`

    Example::

        @make_xp_test_case(f1)
        def test_f1(xp):
            ...

        @make_xp_test_case(f2)
        def test_f2(xp):
            ...

        @make_xp_test_case(f1, f2)
        def test_f1_and_f2(xp):
            ...

    The above is equivalent to::
        @pytest.mark.skip_xp_backends(...)
        @pytest.mark.skip_xp_backends(...)
        @pytest.mark.xfail_xp_backends(...)
        @pytest.mark.xfail_xp_backends(...)
        def test_f1(xp):
            ...

    etc., where the arguments of ``skip_xp_backends`` and ``xfail_xp_backends`` are
    determined by the ``@xp_capabilities`` decorator applied to the functions.

    Notes
    -----

    To allow use of ``make_xp_test_case`` with classes, elements of ``funcs`` may
    also be tuples of the form ``(cls, method_name)`` consisting of a ``type`` and
    a string giving the name of a method. ``lazy_xp_function`` will be applied to the
    method of interest. Capabilities for the method with name ``method_name`` can
    be specified in the ``method_capabilities`` kwarg in the application of
    ``xp_capabilities`` to ``cls``. If no ``method_capabilities`` entry is given
    for ``method_name``, then the capabilities default to the class level
    capabilities.

    Tuples of the form ``(cls, method_name)`` are used instead of ``cls.method`` in
    order to handle inheritance gracefully, since if ``cls`` derives from a parent
    class, ``cls.method`` will be a reference to the parent method, potentially
    causing problems for ``lazy_xp_function``.

    See Also
    --------
    xp_capabilities
    make_xp_pytest_marks
    make_xp_pytest_param
    array_api_extra.testing.lazy_xp_function
    """
    marks = make_xp_pytest_marks(*funcs, capabilities_table=capabilities_table)
    return lambda func: functools.reduce(lambda f, g: g(f), marks, func)

