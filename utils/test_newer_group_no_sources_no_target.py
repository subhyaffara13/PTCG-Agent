
def test_newer_group_no_sources_no_target(tmp_path):
    """
    Consider no sources and no target "newer".
    """
    assert newer_group([], str(tmp_path / 'does-not-exist'))

