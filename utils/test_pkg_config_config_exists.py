
def test_pkg_config_config_exists():
    assert PKG_CONFIG_DIR.joinpath('numpy.pc').is_file()

