
def _mp_prefork(
    plugins: Checkers, options: argparse.Namespace
) -> Generator[None]:
    # we can save significant startup work w/ `fork` multiprocessing
    global _mp_plugins, _mp_options
    _mp_plugins, _mp_options = plugins, options
    try:
        yield
    finally:
        del _mp_plugins, _mp_options

