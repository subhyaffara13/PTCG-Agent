
def test_config_defaults():
    class DefaultConfig(Config):
        x: int = 0
        y: int

    cfg = DefaultConfig(y=1)
    assert cfg.x == 0
    cfg = DefaultConfig(x=2, y=1)
    assert cfg.x == 2

