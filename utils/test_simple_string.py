
def test_simple_string():
    assert m.string_roundtrip("const char *") == "const char *"

