import sys

def test_resolve_class(monkeypatch, tmp_path, package_dir, file, module, return_value):
    monkeypatch.setattr(sys, "modules", {})  # reproducibility
    files = {file: f"class Custom:\n    def testing(self): return {return_value}"}
    write_files(files, tmp_path)
    cls = expand.resolve_class(f"{module}.Custom", package_dir, tmp_path)
    assert cls().testing() == return_value

