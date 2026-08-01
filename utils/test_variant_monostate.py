
def test_variant_monostate(doc):
    assert m.load_monostate_variant(None) == "std::monostate"
    assert m.load_monostate_variant(1) == "int"
    assert m.load_monostate_variant("1") == "std::string"

    assert m.cast_monostate_variant() == (None, 5, "Hello")

    assert (
        doc(m.load_monostate_variant)
        == "load_monostate_variant(arg0: Union[None, int, str]) -> str"
    )

