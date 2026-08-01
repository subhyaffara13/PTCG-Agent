
def test_version_module():
    contents = {s for s in dir(np.version) if not s.startswith('_')}
    expected = {
        'full_version',
        'git_revision',
        'release',
        'short_version',
        'version',
    }

    assert contents == expected

