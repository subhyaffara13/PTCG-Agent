
def test_apply_map_header_raises(mi_styler):
    # GH 41893
    with pytest.raises(ValueError, match="No axis named bad for object type DataFrame"):
        mi_styler.map_index(lambda v: "attr: val;", axis="bad")._compute()

