
def test_fcode_Float():
    assert fcode(Float(42.0)) == "      42.0000000000000d0"
    assert fcode(Float(-1e20)) == "      -1.00000000000000d+20"

