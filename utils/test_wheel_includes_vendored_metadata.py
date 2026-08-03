import os
import re

def test_wheel_includes_vendored_metadata(setuptools_wheel):
    with ZipFile(setuptools_wheel) as zipfile:
        contents = [f.replace(os.sep, '/') for f in zipfile.namelist()]

    assert any(
        re.search(r'_vendor/.*\.dist-info/METADATA', member) for member in contents
    )

