
def test_config_str():
    assert str(cli.Config()) == '{}'
    assert str(cli.Config(a=2)) == '{\'a\': 2}'

