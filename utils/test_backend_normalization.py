
def test_backend_normalization(backend, normalized):
    assert backend_registry._backend_module_name(backend) == normalized

