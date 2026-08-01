
def test_mi_as_xml(mi_config):
    h = harvest.MIHarvester([], mi_config)
    with pytest.raises(NotImplementedError):
        h.as_xml()

