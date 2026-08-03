import os

def test_findall_missing_symlink(tmpdir):
    with tmpdir.as_cwd():
        os.symlink('foo', 'bar')
        found = list(setuptools.findall())
        assert found == []

