
def test_version_submodule_members():
    """`scipy.version` may not be quite public, but we install it.

    So check that we don't silently change its contents.
    """
    for attr in ('version', 'full_version', 'short_version', 'git_revision', 'release'):
        assert hasattr(scipy.version, attr)

