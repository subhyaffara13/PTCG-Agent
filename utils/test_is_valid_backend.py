
def test_is_valid_backend(backend, is_valid):
    assert backend_registry.is_valid_backend(backend) == is_valid

