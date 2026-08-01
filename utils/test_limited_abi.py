
def test_limited_abi(monkeypatch, tmp_path, tmp_path_factory):
    """Test that building a binary wheel with the limited ABI works."""
    source_dir = tmp_path_factory.mktemp("extension_dist")
    (source_dir / "setup.py").write_text(EXTENSION_SETUPPY, encoding="utf-8")
    (source_dir / "extension.c").write_text(EXTENSION_EXAMPLE, encoding="utf-8")
    build_dir = tmp_path.joinpath("build")
    dist_dir = tmp_path.joinpath("dist")
    monkeypatch.chdir(source_dir)
    bdist_wheel_cmd(bdist_dir=str(build_dir), dist_dir=str(dist_dir)).run()

