
def test_config_eq():
    assert cli.Config() == cli.Config()
    assert cli.Config(a=2) == cli.Config(a=2)
    assert cli.Config(a=2) != cli.Config(b=2)

