import os

def test_its_own_wheel_does_not_contain_tests(setuptools_wheel):
    with ZipFile(setuptools_wheel) as zipfile:
        contents = [f.replace(os.sep, '/') for f in zipfile.namelist()]

    for member in contents:
        assert '/tests/' not in member

