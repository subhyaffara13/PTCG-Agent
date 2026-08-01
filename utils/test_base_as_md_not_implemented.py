
def test_base_as_md_not_implemented(base_config):
    h = harvest.Harvester([], base_config)
    with pytest.raises(NotImplementedError):
        h.as_md()

