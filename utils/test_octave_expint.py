
def test_octave_expint():
    assert mcode(expint(1, x)) == "expint(x)"
    with raises(NotImplementedError):
        mcode(expint(2, x))
    assert mcode(expint(y, x), strict=False) == (
        "% Not supported in Octave:\n"
        "% expint\n"
        "expint(y, x)"
    )

