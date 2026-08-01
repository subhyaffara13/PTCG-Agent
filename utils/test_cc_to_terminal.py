
def test_cc_to_terminal(cc_config, mocker):
    reset_mock = mocker.patch('radon.cli.harvest.RESET')
    ranks_mock = mocker.patch('radon.cli.harvest.RANKS_COLORS')
    c2t_mock = mocker.patch('radon.cli.harvest.cc_to_terminal')
    h = harvest.CCHarvester([], cc_config)
    h._results = [('a', {'error': 'mystr'}), ('b', {})]
    c2t_mock.return_value = (['res'], 9, 3)
    ranks_mock.__getitem__.return_value = '<|A|>'
    reset_mock.__eq__.side_effect = lambda o: o == '__R__'

    results = list(h.to_terminal())
    c2t_mock.assert_called_once_with(
        {},
        cc_config.show_complexity,
        cc_config.min,
        cc_config.max,
        cc_config.total_average,
    )
    assert results == [
        ('a', ('mystr',), {'error': True}),
        ('b', (), {}),
        (['res'], (), {'indent': 1}),
        ('\n{0} blocks (classes, functions, methods) analyzed.', (3,), {}),
        (
            'Average complexity: {0}{1} ({2}){3}',
            ('<|A|>', 'A', 3, '__R__'),
            {},
        ),
    ]


def test_cc_to_terminal():
    # do the patching
    tools.LETTERS_COLORS = dict((l, '<!{0}!>'.format(l)) for l in 'FMC')
    tools.RANKS_COLORS = dict((r, '<|{0}|>'.format(r)) for r in 'ABCDEF')
    tools.BRIGHT = '@'
    tools.RESET = '__R__'

    results = CC_TO_TERMINAL_CASES
    res = [
        '@<!C!>C __R__17:0 Classname - <|A|>A (4)__R__',
        '@<!M!>M __R__19:4 Classname.meth - <|B|>B (7)__R__',
        '@<!F!>F __R__12:0 f1 - <|C|>C (14)__R__',
        '@<!F!>F __R__12:0 f2 - <|D|>D (22)__R__',
        '@<!F!>F __R__12:0 f3 - <|E|>E (32)__R__',
        '@<!F!>F __R__12:0 f4 - <|F|>F (41)__R__',
    ]
    res_noshow = ['{0}__R__'.format(r[: r.index('(') - 1]) for r in res]

    assert tools.cc_to_terminal(results, False, 'A', 'F', False) == (
        res_noshow,
        120,
        6,
    )
    assert tools.cc_to_terminal(results, True, 'A', 'F', False) == (
        res,
        120,
        6,
    )
    assert tools.cc_to_terminal(results, True, 'A', 'D', False) == (
        res[:-2],
        47,
        4,
    )
    assert tools.cc_to_terminal(results, False, 'A', 'D', False) == (
        res_noshow[:-2],
        47,
        4,
    )
    assert tools.cc_to_terminal(results, True, 'C', 'F', False) == (
        res[2:],
        109,
        4,
    )
    assert tools.cc_to_terminal(results, True, 'B', 'E', False) == (
        res[1:-1],
        75,
        4,
    )
    assert tools.cc_to_terminal(results, True, 'B', 'F', True) == (
        res[1:],
        120,
        6,
    )

