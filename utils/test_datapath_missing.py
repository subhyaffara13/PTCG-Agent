
def test_datapath_missing(datapath):
    with pytest.raises(ValueError, match="Could not find file"):
        datapath("not_a_file")

