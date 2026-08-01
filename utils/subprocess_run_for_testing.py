
def subprocess_run_for_testing(command, env=None, timeout=60, stdout=None,
                               stderr=None, check=False, text=True,
                               capture_output=False, **kwargs):
    """
    Create and run a subprocess.

    Thin wrapper around `subprocess.run`, intended for testing.  Will
    mark fork() failures on Cygwin as expected failures: not a
    success, but not indicating a problem with the code either.

    Parameters
    ----------
    args : list of str
    env : dict[str, str]
    timeout : float
    stdout, stderr
    check : bool
    text : bool
        Also called ``universal_newlines`` in subprocess.  I chose this
        name since the main effect is returning bytes (`False`) vs. str
        (`True`), though it also tries to normalize newlines across
        platforms.
    capture_output : bool
        Set stdout and stderr to subprocess.PIPE

    Returns
    -------
    proc : subprocess.Popen

    See Also
    --------
    subprocess.run

    Raises
    ------
    pytest.skip
        If running on emscripten, which does not support subprocesses.
    pytest.xfail
        If platform is Cygwin and subprocess reports a fork() failure.
    """
    if sys.platform == 'emscripten':
        import pytest
        pytest.skip('emscripten does not support subprocesses')
    if capture_output:
        stdout = stderr = subprocess.PIPE
    # Add CREATE_NO_WINDOW flag on Windows to prevent console window overhead
    # This is added in an attempt to fix flaky timeouts of subprocesses on Windows
    if sys.platform == 'win32':
        if 'creationflags' not in kwargs:
            kwargs['creationflags'] = subprocess.CREATE_NO_WINDOW
        else:
            kwargs['creationflags'] |= subprocess.CREATE_NO_WINDOW
    try:
        proc = subprocess.run(
            command, env=env,
            timeout=timeout, check=check,
            stdout=stdout, stderr=stderr,
            text=text, **kwargs
        )
    except BlockingIOError:
        if sys.platform == "cygwin":
            # Might want to make this more specific
            import pytest
            pytest.xfail("Fork failure")
        raise
    except subprocess.CalledProcessError as e:
        if e.stdout:
            _log.error(f"Subprocess output:\n{e.stdout}")
        if e.stderr:
            _log.error(f"Subprocess error:\n{e.stderr}")
        raise e
    if proc.stdout:
        _log.debug(f"Subprocess output:\n{proc.stdout}")
    if proc.stderr:
        _log.debug(f"Subprocess error:\n{proc.stderr}")
    return proc

