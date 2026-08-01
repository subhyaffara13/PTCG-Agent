
def test_base_as_xml_not_implemented(base_config):
    h = harvest.Harvester([], base_config)
    with pytest.raises(NotImplementedError):
        h.as_xml()

