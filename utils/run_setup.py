import sys

def run_setup(script_name, script_args: Iterable[str] | None = None, stop_after="run"):
    """Run a setup script in a somewhat controlled environment, and
    return the Distribution instance that drives things.  This is useful
    if you need to find out the distribution meta-data (passed as
    keyword args from 'script' to 'setup()', or the contents of the
    config files or command-line.

    'script_name' is a file that will be read and run with 'exec()';
    'sys.argv[0]' will be replaced with 'script' for the duration of the
    call.  'script_args' is a list of strings; if supplied,
    'sys.argv[1:]' will be replaced by 'script_args' for the duration of
    the call.

    'stop_after' tells 'setup()' when to stop processing; possible
    values:
      init
        stop after the Distribution instance has been created and
        populated with the keyword arguments to 'setup()'
      config
        stop after config files have been parsed (and their data
        stored in the Distribution instance)
      commandline
        stop after the command-line ('sys.argv[1:]' or 'script_args')
        have been parsed (and the data stored in the Distribution)
      run [default]
        stop after all commands have been run (the same as if 'setup()'
        had been called in the usual way

    Returns the Distribution instance, which provides all information
    used to drive the Distutils.
    """
    if stop_after not in ('init', 'config', 'commandline', 'run'):
        raise ValueError(f"invalid value for 'stop_after': {stop_after!r}")

    global _setup_stop_after, _setup_distribution
    _setup_stop_after = stop_after

    save_argv = sys.argv.copy()
    g = {'__file__': script_name, '__name__': '__main__'}
    try:
        try:
            sys.argv[0] = script_name
            if script_args is not None:
                sys.argv[1:] = script_args
            # tokenize.open supports automatic encoding detection
            with tokenize.open(script_name) as f:
                code = f.read().replace(r'\r\n', r'\n')
                exec(code, g)
        finally:
            sys.argv = save_argv
            _setup_stop_after = None
    except SystemExit:
        # Hmm, should we do something if exiting with a non-zero code
        # (ie. error)?
        pass

    if _setup_distribution is None:
        raise RuntimeError(
            "'distutils.core.setup()' was never called -- "
            f"perhaps '{script_name}' is not a Distutils setup script?"
        )

    # I wonder if the setup script's namespace -- g and l -- would be of
    # any interest to callers?
    # print "_setup_distribution:", _setup_distribution
    return _setup_distribution


def run_setup(script_name: str, script_args: list[str]) -> bool:
    """Run a setup script in a somewhat controlled environment.

    This is adapted from code in distutils and our goal here is that is
    faster to not need to spin up a python interpreter to run it.

    We had to fork it because the real run_setup swallows errors
    and KeyboardInterrupt with no way to recover them (!).
    The real version has some extra features that we removed since
    we weren't using them.

    Returns whether the setup succeeded.
    """
    save_argv = sys.argv.copy()
    g = {"__file__": script_name}
    try:
        try:
            sys.argv[0] = script_name
            sys.argv[1:] = script_args
            with open(script_name, "rb") as f:
                exec(f.read(), g)
        finally:
            sys.argv = save_argv
    except SystemExit as e:
        # distutils converts KeyboardInterrupt into a SystemExit with
        # "interrupted" as the argument. Convert it back so that
        # pytest will exit instead of just failing the test.
        if e.code == "interrupted":
            raise KeyboardInterrupt from e

        return e.code == 0 or e.code is None

    return True

