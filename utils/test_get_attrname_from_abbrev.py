
def test_get_attrname_from_abbrev(freqstr, expected):
    reso = Resolution.get_reso_from_freqstr(freqstr)
    assert reso.attr_abbrev == freqstr
    assert reso.attrname == expected

