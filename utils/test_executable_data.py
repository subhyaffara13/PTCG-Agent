import os

def test_executable_data(tmpdir_cwd):
    """
    Ensure executable bit is preserved in copy for
    package data, as users rely on it for scripts.

    #2041
    """
    dist = Distribution(
        dict(
            script_name='setup.py',
            script_args=['build_py'],
            packages=['pkg'],
            package_data={'pkg': ['run-me']},
        )
    )
    os.makedirs('pkg')
    open('pkg/__init__.py', 'wb').close()
    open('pkg/run-me', 'wb').close()
    os.chmod('pkg/run-me', 0o700)

    dist.parse_command_line()
    dist.run_commands()

    assert os.stat('build/lib/pkg/run-me').st_mode & stat.S_IEXEC, (
        "Script is not executable"
    )

