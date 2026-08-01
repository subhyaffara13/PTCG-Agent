
def test_sys_exit_0_in_setuppy(monkeypatch, tmp_path):
    """Setuptools should be resilient to setup.py with ``sys.exit(0)`` (#3973)."""
    monkeypatch.chdir(tmp_path)
    setuppy = """
        import sys, setuptools
        setuptools.setup(name='foo', version='0.0.0')
        sys.exit(0)
        """
    (tmp_path / "setup.py").write_text(DALS(setuppy), encoding="utf-8")
    backend = BuildBackend(backend_name="setuptools.build_meta")
    assert backend.get_requires_for_build_wheel() == []

