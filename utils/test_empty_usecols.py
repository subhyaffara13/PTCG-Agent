
def test_empty_usecols(all_parsers):
    data = "a,b,c\n1,2,3\n4,5,6"
    expected = DataFrame(columns=Index([]))
    parser = all_parsers

    result = parser.read_csv(StringIO(data), usecols=set())
    tm.assert_frame_equal(result, expected)


def test_empty_usecols():
    txt = StringIO("0,0,XXX\n0,XXX,0,XXX\n0,XXX,XXX,0,XXX\n")
    res = np.loadtxt(txt, dtype=np.dtype([]), delimiter=",", usecols=[])
    assert res.shape == (3,)
    assert res.dtype == np.dtype([])

