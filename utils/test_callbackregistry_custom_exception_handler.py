
def test_callbackregistry_custom_exception_handler(monkeypatch, cb, excp):
    monkeypatch.setattr(
        cbook, "_get_running_interactive_framework", lambda: None)
    with pytest.raises(excp):
        cb.process('foo')

