import sys

def test_no_ctypes(monkeypatch) -> None:
    def _fake_import(name: str, *args, **kwargs):
        if name == "ctypes":
            raise ModuleNotFoundError(f"No module named {name}")

        return importlib.__import__(name, *args, **kwargs)

    with suppress(KeyError):
        monkeypatch.delitem(sys.modules, "wheel.macosx_libfile")

    # Install an importer shim that refuses to load ctypes
    monkeypatch.setattr(builtins, "__import__", _fake_import)
    with pytest.raises(ModuleNotFoundError, match="No module named ctypes"):
        import wheel.macosx_libfile  # noqa: F401

    # Unload and reimport the bdist_wheel command module to make sure it won't try to
    # import ctypes
    monkeypatch.delitem(sys.modules, "setuptools.command.bdist_wheel")

    import setuptools.command.bdist_wheel  # noqa: F401

