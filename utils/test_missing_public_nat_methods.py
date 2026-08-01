
def test_missing_public_nat_methods(klass, expected):
    # see gh-17327
    #
    # NaT should have *most* of the Timestamp and Timedelta methods.
    # Here, we check which public methods NaT does not have. We
    # ignore any missing private methods.
    nat_names = dir(NaT)
    klass_names = dir(klass)

    missing = [x for x in klass_names if x not in nat_names and not x.startswith("_")]
    missing.sort()

    assert missing == expected

