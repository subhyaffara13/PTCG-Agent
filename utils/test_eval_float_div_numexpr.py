
def test_eval_float_div_numexpr():
    # GH 59736
    result = pd.eval("1 / 2", engine="numexpr")
    expected = 0.5
    assert result == expected

