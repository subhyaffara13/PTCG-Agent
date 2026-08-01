
def test_resolve_gui_or_backend_invalid():
    match = "is not a recognised GUI loop or backend name"
    with pytest.raises(RuntimeError, match=match):
        backend_registry.resolve_gui_or_backend('no-such-name')

