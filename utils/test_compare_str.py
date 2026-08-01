
def test_compare_str(_offset):
    # GH#23524
    # comparing to strings that cannot be cast to DateOffsets should
    #  not raise for __eq__ or __ne__
    off = _get_offset(_offset)

    assert not off == "infer"
    assert off != "foo"

