
def test_pretty_SetExpr():
    iv = Interval(1, 3)
    se = SetExpr(iv)
    ascii_str = "SetExpr([1, 3])"
    ucode_str = "SetExpr([1, 3])"
    assert pretty(se) == ascii_str
    assert upretty(se) == ucode_str

