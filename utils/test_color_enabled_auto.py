
def test_color_enabled_auto(monkeypatch, mocker):
    monkeypatch.setenv("COLOR", "auto")
    isatty_mock = mocker.patch('sys.stdout.isatty')

    isatty_mock.return_value = True
    assert colors.color_enabled()

    isatty_mock.return_value = False
    assert not colors.color_enabled()

