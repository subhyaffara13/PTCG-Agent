
def test_missing_required_dependency(monkeypatch, dependency):
    # GH#61030
    original_import = __import__
    mock_error = ImportError(f"Mock error for {dependency}")

    def mock_import(name, *args, **kwargs):
        if name == dependency:
            raise mock_error
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr("builtins.__import__", mock_import)

    with pytest.raises(ImportError, match=dependency):
        importlib.reload(importlib.import_module("pandas"))

