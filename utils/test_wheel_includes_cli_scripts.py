
def test_wheel_includes_cli_scripts(setuptools_wheel):
    with ZipFile(setuptools_wheel) as zipfile:
        contents = [f.replace(os.sep, '/') for f in zipfile.namelist()]

    assert any('cli-64.exe' in member for member in contents)

