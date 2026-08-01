
def test_verbosity_level(tmp_path, monkeypatch, flags, expected_level):
    """Make sure the correct verbosity level is set (issue #3038)"""
    import setuptools  # noqa: F401  # import setuptools to monkeypatch distutils

    import distutils  # <- load distutils after all the patches take place

    logger = logging.Logger(__name__)
    monkeypatch.setattr(logging, "root", logger)
    unset_log_level = logger.getEffectiveLevel()
    assert logging.getLevelName(unset_log_level) == "NOTSET"

    setup_script = tmp_path / "setup.py"
    setup_script.write_text(setup_py, encoding="utf-8")
    dist = distutils.core.run_setup(setup_script, stop_after="init")
    dist.script_args = flags + ["sdist"]
    dist.parse_command_line()  # <- where the log level is set
    log_level = logger.getEffectiveLevel()
    log_level_name = logging.getLevelName(log_level)
    assert log_level_name == expected_level

