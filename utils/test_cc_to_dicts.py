
def test_cc_to_dicts(cc_config, mocker):
    c2d_mock = mocker.patch('radon.cli.harvest.cc_to_dict')
    c2d_mock.side_effect = lambda i: i
    h = harvest.CCHarvester([], cc_config)
    sample_results = [
        ('a', [{'rank': 'A'}]),
        ('b', [{'rank': 'B'}]),
        ('c', {'error': 'An ERROR!'}),
    ]
    h._results = sample_results

    assert h._to_dicts() == dict(sample_results)
    assert c2d_mock.call_count == 2

    h.config.min = 'B'
    h._results = sample_results[1:]
    assert h._to_dicts() == dict(sample_results[1:])

