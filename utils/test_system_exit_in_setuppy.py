
def test_system_exit_in_setuppy(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    setuppy = "import sys; sys.exit('some error')"
    (tmp_path / "setup.py").write_text(setuppy, encoding="utf-8")
    with pytest.raises(SystemExit, match="some error"):
        backend = BuildBackend(backend_name="setuptools.build_meta")
        backend.get_requires_for_build_wheel()

