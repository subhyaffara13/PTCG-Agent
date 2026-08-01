
def test_elem_and_attrs_only(kml_cta_rail_lines, parser):
    with pytest.raises(
        ValueError,
        match=("Either element or attributes can be parsed not both"),
    ):
        read_xml(kml_cta_rail_lines, elems_only=True, attrs_only=True, parser=parser)

