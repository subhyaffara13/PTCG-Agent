
def test_config_base_behavior():
    c = cli.Config(a=2, b=3)
    assert c.config_values == {'a': 2, 'b': 3}
    assert c.a == 2
    assert c.b == 3

