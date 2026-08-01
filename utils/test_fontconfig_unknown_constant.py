
def test_fontconfig_unknown_constant():
    with pytest.raises(ValueError, match="ParseException"):
        FontProperties(":unknown")

