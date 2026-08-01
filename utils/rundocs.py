
def rundocs(filename=None, raise_on_error=True):
    """
    Run doctests found in the given file.

    By default `rundocs` raises an AssertionError on failure.

    Parameters
    ----------
    filename : str
        The path to the file for which the doctests are run.
    raise_on_error : bool
        Whether to raise an AssertionError when a doctest fails. Default is
        True.

    Notes
    -----
    The doctests can be run by the user/developer by adding the ``doctests``
    argument to the ``test()`` call. For example, to run all tests (including
    doctests) for ``numpy.lib``:

    >>> np.lib.test(doctests=True)  # doctest: +SKIP
    """
    import doctest

    if filename is None:
        f = sys._getframe(1)
        filename = f.f_globals['__file__']
    name = os.path.splitext(os.path.basename(filename))[0]
    spec = importlib.util.spec_from_file_location(name, filename)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)

    tests = doctest.DocTestFinder().find(m)
    runner = doctest.DocTestRunner(verbose=False)

    msg = []
    if raise_on_error:
        out = msg.append
    else:
        out = None

    for test in tests:
        runner.run(test, out=out)

    if runner.failures > 0 and raise_on_error:
        err_msg = '\n'.join(msg)
        raise AssertionError(f"Some doctests failed:\n{err_msg}")

