
def test_quotechar_multichar_error():
    txt = StringIO("1,2\n3,4")
    msg = r".*must be a single unicode character or None"
    with pytest.raises(TypeError, match=msg):
        np.loadtxt(txt, delimiter=",", quotechar="''")

