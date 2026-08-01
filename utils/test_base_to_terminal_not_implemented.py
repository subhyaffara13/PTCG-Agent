
def test_base_to_terminal_not_implemented(base_config):
    h = harvest.Harvester([], base_config)
    with pytest.raises(NotImplementedError):
        h.to_terminal()

