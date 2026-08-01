
def show_fixtures_per_test(config: Config) -> int | ExitCode:
    from _pytest.main import wrap_session

    return wrap_session(config, _show_fixtures_per_test)

