
def test_mi_as_json(mi_config, mocker):
    d_mock = mocker.patch('radon.cli.harvest.json.dumps')
    h = harvest.MIHarvester([], mi_config)
    h.config.min = 'C'
    h._results = [
        ('a', {'error': 'mystr'}),
        ('b', {'mi': 25, 'rank': 'A'}),
        ('c', {'mi': 15, 'rank': 'B'}),
        ('d', {'mi': 0, 'rank': 'C'}),
    ]

    h.as_json()
    d_mock.assert_called_with(dict([h._results[0], h._results[-1]]))

