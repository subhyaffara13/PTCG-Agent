
def test_metadata_immutable(idx):
    levels, codes = idx.levels, idx.codes
    # shouldn't be able to set at either the top level or base level
    mutable_regex = re.compile("does not support mutable operations")
    with pytest.raises(TypeError, match=mutable_regex):
        levels[0] = levels[0]
    with pytest.raises(TypeError, match=mutable_regex):
        levels[0][0] = levels[0][0]
    # ditto for labels
    with pytest.raises(TypeError, match=mutable_regex):
        codes[0] = codes[0]
    with pytest.raises(ValueError, match="assignment destination is read-only"):
        codes[0][0] = codes[0][0]
    # and for names
    names = idx.names
    with pytest.raises(TypeError, match=mutable_regex):
        names[0] = names[0]

