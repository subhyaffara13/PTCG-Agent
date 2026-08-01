
def test_mi_to_terminal(mi_config, mocker):
    reset_mock = mocker.patch('radon.cli.harvest.RESET')
    ranks_mock = mocker.patch('radon.cli.harvest.MI_RANKS')
    ranks_mock.__getitem__.side_effect = lambda j: '<|{0}|>'.format(j)
    reset_mock.__eq__.side_effect = lambda o: o == '__R__'

    h = harvest.MIHarvester([], mi_config)
    h._results = [
        ('a', {'error': 'mystr'}),
        ('b', {'mi': 25, 'rank': 'A'}),
        ('c', {'mi': 15, 'rank': 'B'}),
        ('d', {'mi': 0, 'rank': 'C'}),
    ]

    assert list(h.to_terminal()) == [
        ('a', ('mystr',), {'error': True}),
        ('{0} - {1}{2}{3}{4}', ('c', '<|B|>', 'B', ' (15.00)', '__R__'), {}),
        ('{0} - {1}{2}{3}{4}', ('d', '<|C|>', 'C', ' (0.00)', '__R__'), {}),
    ]

