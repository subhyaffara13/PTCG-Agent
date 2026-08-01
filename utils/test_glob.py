
def test_glob(monkeypatch, tmpdir, tree, pattern, matches):
    monkeypatch.chdir(tmpdir)
    path.build({name: '' for name in tree.split()})
    assert list(sorted(glob(pattern))) == list(sorted(matches))

