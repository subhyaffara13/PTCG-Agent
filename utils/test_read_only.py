import os

def test_read_only(tmpdir_cwd):
    """
    Ensure read-only flag is not preserved in copy
    for package modules and package data, as that
    causes problems with deleting read-only files on
    Windows.

    #1451
    """
    dist = Distribution(
        dict(
            script_name='setup.py',
            script_args=['build_py'],
            packages=['pkg'],
            package_data={'pkg': ['data.dat']},
        )
    )
    os.makedirs('pkg')
    open('pkg/__init__.py', 'wb').close()
    open('pkg/data.dat', 'wb').close()
    os.chmod('pkg/__init__.py', stat.S_IREAD)
    os.chmod('pkg/data.dat', stat.S_IREAD)
    dist.parse_command_line()
    dist.run_commands()
    shutil.rmtree('build')

