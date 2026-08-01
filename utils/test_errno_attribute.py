
def test_errno_attribute():
    # GH 13872
    with pytest.raises(FileNotFoundError, match="\\[Errno 2\\]") as err:
        pd.read_csv("doesnt_exist")
        assert err.errno == errno.ENOENT

