
def test_base_as_json(base_config):
    h = harvest.Harvester([], base_config)
    h._results = {'filename': {'complexity': 2}}
    assert h.as_json() == '{"filename": {"complexity": 2}}'

