
def run_and_exit(*args, **kwargs):
    """Run the tests, and if there are failures, exit with a return code of 1.

    This is needed for various buildbots to recognise that the tests have
    failed.
    """
    total, fails = run(*args, **kwargs)
    if fails:
        sys.exit(1)
    sys.exit(0)

