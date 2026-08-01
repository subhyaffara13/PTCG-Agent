
def test_cross_Qt_imports(host, mpl):
    try:
        proc = _run_helper(_impl_test_cross_Qt_imports, host, mpl,
                           timeout=_test_timeout)
    except subprocess.CalledProcessError as ex:
        # We do try to warn the user they are doing something that we do not
        # expect to work, so we're going to ignore if the subprocess crashes or
        # is killed, and just check that the warning is printed.
        stderr = ex.stderr
    else:
        stderr = proc.stderr
    assert "Mixing Qt major versions may not work as expected." in stderr

