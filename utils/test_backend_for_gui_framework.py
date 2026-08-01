
def test_backend_for_gui_framework(framework, expected):
    assert backend_registry.backend_for_gui_framework(framework) == expected

