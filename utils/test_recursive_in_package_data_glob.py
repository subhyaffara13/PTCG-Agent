import os

def test_recursive_in_package_data_glob(tmpdir_cwd):
    """
    Files matching recursive globs (**) in package_data should
    be included in the package data.

    #1806
    """
    dist = Distribution(
        dict(
            script_name='setup.py',
            script_args=['build_py'],
            packages=[''],
            package_data={'': ['path/**/data']},
        )
    )
    os.makedirs('path/subpath/subsubpath')
    open('path/subpath/subsubpath/data', 'wb').close()

    dist.parse_command_line()
    dist.run_commands()

    assert stat.S_ISREG(os.stat('build/lib/path/subpath/subsubpath/data').st_mode), (
        "File is not included"
    )

