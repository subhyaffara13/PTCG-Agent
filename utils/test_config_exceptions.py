
def test_config_exceptions():
    c = cli.Config(a=2)
    assert c.__dict__, {'config_values': {'a': 2}}
    with pytest.raises(AttributeError):
        c.notexistent

