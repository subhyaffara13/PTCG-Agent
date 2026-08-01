
def _mp_run(filename: str) -> tuple[str, Results, dict[str, int]]:
    return FileChecker(
        filename=filename, plugins=_mp_plugins, options=_mp_options
    ).run_checks()

