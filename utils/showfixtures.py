
def showfixtures(config: Config) -> int | ExitCode:
    from _pytest.main import wrap_session

    return wrap_session(config, _showfixtures_main)

