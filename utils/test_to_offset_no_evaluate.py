
def test_to_offset_no_evaluate():
    msg = str(("", ""))
    with pytest.raises(TypeError, match=msg):
        to_offset(("", ""))

