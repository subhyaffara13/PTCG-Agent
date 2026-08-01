
def test_read_huge_row():
    row = "1.5, 2.5," * 50000
    row = row[:-1] + "\n"
    txt = StringIO(row * 2)
    res = np.loadtxt(txt, delimiter=",", dtype=float)
    assert_equal(res, np.tile([1.5, 2.5], (2, 50000)))

