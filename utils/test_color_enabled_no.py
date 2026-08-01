
def test_color_enabled_no(monkeypatch):
    monkeypatch.setenv("COLOR", "no")
    assert not colors.color_enabled()

