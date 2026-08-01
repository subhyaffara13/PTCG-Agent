
def all_ok_test(suite, *args):
    for results in args:
        assert "Ran 36 tests" in results  # some tests are running
        assert "OK" in results  # OK

