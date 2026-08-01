
def test__rng_html_rewrite():
    def mock_str():
        lines = [
            'np.random.default_rng(8989843)',
            'np.random.default_rng(seed)',
            'np.random.default_rng(0x9a71b21474694f919882289dc1559ca)',
            ' bob ',
        ]
        return lines

    res = _rng_html_rewrite(mock_str)()
    ref = [
        'np.random.default_rng()',
        'np.random.default_rng(seed)',
        'np.random.default_rng()',
        ' bob ',
    ]

    assert res == ref

