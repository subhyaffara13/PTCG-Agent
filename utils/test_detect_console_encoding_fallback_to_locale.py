
def test_detect_console_encoding_fallback_to_locale(monkeypatch, encoding):
    # GH 21552
    with monkeypatch.context() as context:
        context.setattr("locale.getpreferredencoding", lambda: "foo")
        context.setattr("sys.stdout", MockEncoding(encoding))
        assert detect_console_encoding() == "foo"

