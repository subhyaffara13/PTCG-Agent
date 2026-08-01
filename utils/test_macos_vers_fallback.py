
def test_macos_vers_fallback(monkeypatch, tmp_path):
    """Regression test for pkg_resources._macos_vers"""
    orig_open = builtins.open

    # Pretend we need to use the plist file
    monkeypatch.setattr('platform.mac_ver', mock.Mock(return_value=('', (), '')))

    # Create fake content for the fake plist file
    with open(tmp_path / 'fake.plist', 'wb') as fake_file:
        plistlib.dump({"ProductVersion": "11.4"}, fake_file)

    # Pretend the fake file exists
    monkeypatch.setattr('os.path.exists', mock.Mock(return_value=True))

    def fake_open(file, *args, **kwargs):
        return orig_open(tmp_path / 'fake.plist', *args, **kwargs)

    # Ensure that the _macos_vers works correctly
    with mock.patch('builtins.open', mock.Mock(side_effect=fake_open)) as m:
        pkg_resources._macos_vers.cache_clear()
        assert pkg_resources._macos_vers() == ["11", "4"]
        pkg_resources._macos_vers.cache_clear()

    m.assert_called()

