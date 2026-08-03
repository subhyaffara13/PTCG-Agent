import subprocess

def doctest(*paths, subprocess=True, rerun=0, **kwargs):
    r"""
    Runs doctests in all \*.py files in the SymPy directory which match
    any of the given strings in ``paths`` or all tests if paths=[].

    Notes:

    - Paths can be entered in native system format or in unix,
      forward-slash format.
    - Files that are on the blacklist can be tested by providing
      their path; they are only excluded if no paths are given.

    Examples
    ========

    >>> import sympy

    Run all tests:

    >>> sympy.doctest() # doctest: +SKIP

    Run one file:

    >>> sympy.doctest("sympy/core/basic.py") # doctest: +SKIP
    >>> sympy.doctest("polynomial.rst") # doctest: +SKIP

    Run all tests in sympy/functions/ and some particular file:

    >>> sympy.doctest("/functions", "basic.py") # doctest: +SKIP

    Run any file having polynomial in its name, doc/src/modules/polynomial.rst,
    sympy/functions/special/polynomials.py, and sympy/polys/polynomial.py:

    >>> sympy.doctest("polynomial") # doctest: +SKIP

    The ``split`` option can be passed to split the test run into parts. The
    split currently only splits the test files, though this may change in the
    future. ``split`` should be a string of the form 'a/b', which will run
    part ``a`` of ``b``. Note that the regular doctests and the Sphinx
    doctests are split independently. For instance, to run the first half of
    the test suite:

    >>> sympy.doctest(split='1/2')  # doctest: +SKIP

    The ``subprocess`` and ``verbose`` options are the same as with the function
    ``test()`` (see the docstring of that function for more information) except
    that ``verbose`` may also be set equal to ``2`` in order to print
    individual doctest lines, as they are being tested.
    """
    # count up from 0, do not print 0
    print_counter = lambda i : (print("rerun %d" % (rerun-i))
                                if rerun-i else None)

    if subprocess:
        # loop backwards so last i is 0
        for i in range(rerun, -1, -1):
            print_counter(i)
            ret = run_in_subprocess_with_hash_randomization("_doctest",
                        function_args=paths, function_kwargs=kwargs)
            if ret is False:
                break
            val = not bool(ret)
            # exit on the first failure or if done
            if not val or i == 0:
                return val

    # rerun even if hash randomization is not supported
    for i in range(rerun, -1, -1):
        print_counter(i)
        val = not bool(_doctest(*paths, **kwargs))
        if not val or i == 0:
            return val


def doctest():
    """Interface to run doctests via pytest compatible with SymPy's test runner.
    """
    raise NotImplementedError

