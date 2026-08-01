
def test_dispatcher():
    f = Dispatcher('f')
    f.add((int,), inc)
    f.add((float,), dec)

    with warns(DeprecationWarning, test_stacklevel=False):
        assert f.resolve((int,)) == inc
    assert f.dispatch(int) is inc

    assert f(1) == 2
    assert f(1.0) == 0.0


def test_dispatcher():
    """
    Testing the utilities of the CPU dispatcher
    """
    targets = (
        "X86_V2", "X86_V3",
        "VSX", "VSX2", "VSX3",
        "NEON", "ASIMD", "ASIMDHP",
        "VX", "VXE", "LSX", "RVV"
    )
    highest_sfx = ""  # no suffix for the baseline
    all_sfx = []
    for feature in reversed(targets):
        # skip baseline features, by the default `CCompilerOpt` do not generate
        # separated objects for the baseline, just one object combined all of them
        # via 'baseline' option within the configuration statements.
        if feature in __cpu_baseline__:
            continue
        # check compiler and running machine support
        if feature not in __cpu_dispatch__ or not __cpu_features__[feature]:
            continue

        if not highest_sfx:
            highest_sfx = "_" + feature
        all_sfx.append("func" + "_" + feature)

    test = _umath_tests.test_dispatch()
    assert_equal(test["func"], "func" + highest_sfx)
    assert_equal(test["var"], "var" + highest_sfx)

    if highest_sfx:
        assert_equal(test["func_xb"], "func" + highest_sfx)
        assert_equal(test["var_xb"], "var" + highest_sfx)
    else:
        assert_equal(test["func_xb"], "nobase")
        assert_equal(test["var_xb"], "nobase")

    all_sfx.append("func")  # add the baseline
    assert_equal(test["all"], all_sfx)

