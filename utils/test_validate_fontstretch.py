
def test_validate_fontstretch(stretch, parsed_stretch):
    if parsed_stretch is ValueError:
        with pytest.raises(ValueError):
            validate_fontstretch(stretch)
    else:
        assert validate_fontstretch(stretch) == parsed_stretch

