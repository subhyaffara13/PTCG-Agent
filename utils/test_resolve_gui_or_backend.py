
def test_resolve_gui_or_backend(gui_or_backend, expected_backend, expected_gui):
    backend, gui = backend_registry.resolve_gui_or_backend(gui_or_backend)
    assert backend == expected_backend
    assert gui == expected_gui

