import sys

def run_all_tests(test_args=(), test_kwargs=None,
                  doctest_args=(), doctest_kwargs=None,
                  examples_args=(), examples_kwargs=None):
    """
    Run all tests.

    Right now, this runs the regular tests (bin/test), the doctests
    (bin/doctest), and the examples (examples/all.py).

    This is what ``setup.py test`` uses.

    You can pass arguments and keyword arguments to the test functions that
    support them (for now, test,  doctest, and the examples). See the
    docstrings of those functions for a description of the available options.

    For example, to run the solvers tests with colors turned off:

    >>> from sympy.testing.runtests import run_all_tests
    >>> run_all_tests(test_args=("solvers",),
    ... test_kwargs={"colors:False"}) # doctest: +SKIP

    """
    tests_successful = True

    test_kwargs = test_kwargs or {}
    doctest_kwargs = doctest_kwargs or {}
    examples_kwargs = examples_kwargs or {'quiet': True}

    try:
        # Regular tests
        if not test(*test_args, **test_kwargs):
            # some regular test fails, so set the tests_successful
            # flag to false and continue running the doctests
            tests_successful = False

        # Doctests
        print()
        if not doctest(*doctest_args, **doctest_kwargs):
            tests_successful = False

        # Examples
        print()
        sys.path.append("examples")   # examples/all.py
        from all import run_examples  # type: ignore
        if not run_examples(*examples_args, **examples_kwargs):
            tests_successful = False

        if tests_successful:
            return
        else:
            # Return nonzero exit code
            sys.exit(1)
    except KeyboardInterrupt:
        print()
        print("DO *NOT* COMMIT!")
        sys.exit(1)

