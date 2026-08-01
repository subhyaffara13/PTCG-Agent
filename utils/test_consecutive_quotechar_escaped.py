
def test_consecutive_quotechar_escaped():
    txt = StringIO('"Hello, my name is ""Monty""!"')
    expected = np.array('Hello, my name is "Monty"!', dtype="U40")
    res = np.loadtxt(txt, dtype="U40", delimiter=",", quotechar='"')
    assert_equal(res, expected)

