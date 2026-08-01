
def test_config_for():
    assert cli.Config.from_function(func) == cli.Config(b=2, c=[], d=None)
    assert cli.Config.from_function(func2) == cli.Config()
    assert cli.Config.from_function(func3) == cli.Config(b=3)

