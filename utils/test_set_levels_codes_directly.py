
def test_set_levels_codes_directly(idx):
    # setting levels/codes directly raises AttributeError

    levels = idx.levels
    new_levels = [[lev + "a" for lev in level] for level in levels]

    codes = idx.codes
    major_codes, minor_codes = codes
    major_codes = [(x + 1) % 3 for x in major_codes]
    minor_codes = [(x + 1) % 1 for x in minor_codes]
    new_codes = [major_codes, minor_codes]

    msg = "Can't set attribute"
    with pytest.raises(AttributeError, match=msg):
        idx.levels = new_levels

    msg = "property 'codes' of 'MultiIndex' object has no setter"
    with pytest.raises(AttributeError, match=msg):
        idx.codes = new_codes

