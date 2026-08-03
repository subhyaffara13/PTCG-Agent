import re

def test_replace_literal_compiled_raises(any_string_dtype):
    ser = Series([], dtype=any_string_dtype)
    pat = re.compile("[a-z][A-Z]{2}")

    msg = "Cannot use a compiled regex as replacement pattern with regex=False"
    with pytest.raises(ValueError, match=msg):
        ser.str.replace(pat, "", regex=False)

