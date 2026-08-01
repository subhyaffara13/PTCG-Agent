
def test_color_enabled_yes(monkeypatch):
    monkeypatch.setenv("COLOR", "yes")
    assert colors.color_enabled()

