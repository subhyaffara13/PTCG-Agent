
def test_locale_comma():
    # On some systems/pytest versions, `pytest.skip` in an exception handler
    # does not skip, but is treated as an exception, so directly running this
    # test can incorrectly fail instead of skip.
    # Instead, run this test in a subprocess, which avoids the problem, and the
    # need to fix the locale after.
    proc = mpl.testing.subprocess_run_helper(_impl_locale_comma, timeout=60,
                                             extra_env={'MPLBACKEND': 'Agg'})
    skip_msg = next((line[len('SKIP:'):].strip()
                     for line in proc.stdout.splitlines()
                     if line.startswith('SKIP:')),
                    '')
    if skip_msg:
        pytest.skip(skip_msg)

