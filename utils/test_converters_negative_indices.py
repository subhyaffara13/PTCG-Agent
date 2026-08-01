
def test_converters_negative_indices():
    txt = StringIO('1.5,2.5\n3.0,XXX\n5.5,6.0')
    conv = {-1: lambda s: np.nan if s == 'XXX' else float(s)}
    expected = np.array([[1.5, 2.5], [3.0, np.nan], [5.5, 6.0]])
    res = np.loadtxt(txt, dtype=np.float64, delimiter=",", converters=conv)
    assert_equal(res, expected)

