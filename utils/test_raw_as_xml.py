
def test_raw_as_xml(raw_config):
    h = harvest.RawHarvester([], raw_config)
    with pytest.raises(NotImplementedError):
        h.as_xml()

