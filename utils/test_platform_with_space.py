
def test_platform_with_space(dummy_dist, monkeypatch):
    """Ensure building on platforms with a space in the name succeed."""
    monkeypatch.chdir(dummy_dist)
    bdist_wheel_cmd(plat_name="isilon onefs").run()

