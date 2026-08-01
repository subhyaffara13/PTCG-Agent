
def test_not_present_exception():
    msg = "`Import fsspec` failed.  Use pip or conda to install the fsspec package."
    with pytest.raises(ImportError, match=msg):
        read_csv("memory://test/test.csv")

