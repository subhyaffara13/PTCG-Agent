
def test_findall_curdir(example_source):
    with example_source.as_cwd():
        found = list(setuptools.findall())
    expected = ['readme.txt', os.path.join('foo', 'bar.py')]
    assert found == expected

