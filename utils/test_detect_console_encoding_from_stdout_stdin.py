
def test_detect_console_encoding_from_stdout_stdin(monkeypatch, empty, filled):
    # Ensures that when sys.stdout.encoding or sys.stdin.encoding is used when
    # they have values filled.
    # GH 21552
    with monkeypatch.context() as context:
        context.setattr(f"sys.{empty}", MockEncoding(""))
        context.setattr(f"sys.{filled}", MockEncoding(filled))
        assert detect_console_encoding() == filled

