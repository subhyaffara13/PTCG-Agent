
def test_text_language_invalid(input, match):
    with pytest.raises(TypeError, match=match):
        Text(0, 0, 'foo', language=input)

