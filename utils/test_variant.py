
def test_variant(doc):
    assert m.load_variant(1) == "int"
    assert m.load_variant("1") == "std::string"
    assert m.load_variant(1.0) == "double"
    assert m.load_variant(None) == "std::nullptr_t"

    assert m.load_variant_2pass(1) == "int"
    assert m.load_variant_2pass(1.0) == "double"

    assert m.cast_variant() == (5, "Hello")

    assert (
        doc(m.load_variant) == "load_variant(arg0: Union[int, str, float, None]) -> str"
    )

