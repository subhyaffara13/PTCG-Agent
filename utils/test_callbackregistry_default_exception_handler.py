
def test_callbackregistry_default_exception_handler(capsys, monkeypatch):
    cb = cbook.CallbackRegistry()
    cb.connect("foo", lambda: None)

    monkeypatch.setattr(
        cbook, "_get_running_interactive_framework", lambda: None)
    with pytest.raises(TypeError):
        cb.process("foo", "argument mismatch")
    outerr = capsys.readouterr()
    assert outerr.out == outerr.err == ""

    monkeypatch.setattr(
        cbook, "_get_running_interactive_framework", lambda: "not-none")
    cb.process("foo", "argument mismatch")  # No error in that case.
    outerr = capsys.readouterr()
    assert outerr.out == ""
    assert "takes 0 positional arguments but 1 was given" in outerr.err

