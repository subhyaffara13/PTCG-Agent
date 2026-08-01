
def test_detect_console_encoding_fallback_to_default(monkeypatch, std, locale):
    # When both the stdout/stdin encoding and locale preferred encoding checks
    # fail (or return 'ascii', we should default to the sys default encoding.
    # GH 21552
    with monkeypatch.context() as context:
        context.setattr(
            "locale.getpreferredencoding", lambda: MockEncoding.raise_or_return(locale)
        )
        context.setattr("sys.stdout", MockEncoding(std))
        context.setattr("sys.getdefaultencoding", lambda: "sysDefaultEncoding")
        assert detect_console_encoding() == "sysDefaultEncoding"

