
def test_boxstyle_errors(fmt, match):
    with pytest.raises(ValueError, match=match):
        BoxStyle(fmt)

