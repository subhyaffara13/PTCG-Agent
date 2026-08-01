
def test_base_run(base_config):
    h = harvest.Harvester(['-'], base_config)
    h.gobble = fake_gobble
    assert isinstance(h.run(), collections_abc.Iterator)
    assert list(h.run()) == [('-', 42)]
    h.gobble = fake_gobble_raising
    assert list(h.run()) == [('-', {'error': 'mystr'})]

