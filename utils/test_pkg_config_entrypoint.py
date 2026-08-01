
def test_pkg_config_entrypoint():
    (entrypoint,) = importlib.metadata.entry_points(group='pkg_config', name='numpy')
    assert entrypoint.value == numpy._core.lib.pkgconfig.__name__

