
def test_base_results(base_config):
    h = harvest.Harvester([], base_config)
    h.run = fake_run
    results = h.results
    assert isinstance(results, collections_abc.Iterator)
    assert list(results) == [{'file-0': 0}, {'file-1': 1}, {'file-2': 4}]
    assert not isinstance(h.results, collections_abc.Iterator)
    assert isinstance(h.results, collections_abc.Iterable)
    assert isinstance(h.results, list)

