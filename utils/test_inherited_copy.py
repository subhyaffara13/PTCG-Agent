
def test_inherited_copy(mi_styler, deepcopy):
    # Ensure that the inherited class is preserved when a Styler object is copied.
    # GH 52728
    class CustomStyler(Styler):
        pass

    custom_styler = CustomStyler(mi_styler.data)
    custom_styler_copy = (
        copy.deepcopy(custom_styler) if deepcopy else copy.copy(custom_styler)
    )
    assert isinstance(custom_styler_copy, CustomStyler)

