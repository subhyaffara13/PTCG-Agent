
def test_dist_info_is_not_dir(tmp_path, only):
    """Test path containing a file with dist-info extension."""
    dist_info = tmp_path / 'foobar.dist-info'
    dist_info.touch()
    assert not pkg_resources.dist_factory(str(tmp_path), str(dist_info), only)

