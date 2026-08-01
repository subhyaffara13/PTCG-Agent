
def test_base_gobble_not_implemented(base_config):
    h = harvest.Harvester([], base_config)
    with pytest.raises(NotImplementedError):
        h.gobble(None)

