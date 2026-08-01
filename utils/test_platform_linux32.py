
def test_platform_linux32(reported, expected, monkeypatch):
    monkeypatch.setattr(struct, "calcsize", lambda x: 4)
    dist = setuptools.Distribution()
    cmd = bdist_wheel(dist)
    cmd.plat_name = reported
    cmd.root_is_pure = False
    _, _, actual = cmd.get_tag()
    assert actual == expected

