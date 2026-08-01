
def example_source(tmpdir):
    tmpdir.mkdir('foo')
    (tmpdir / 'foo/bar.py').write('')
    (tmpdir / 'readme.txt').write('')
    return tmpdir

