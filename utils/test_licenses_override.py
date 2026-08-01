
def test_licenses_override(dummy_dist, monkeypatch, tmp_path, config_file, config):
    dummy_dist.joinpath(config_file).write_text(config, encoding="utf-8")
    monkeypatch.chdir(dummy_dist)
    bdist_wheel_cmd(bdist_dir=str(tmp_path)).run()
    with ZipFile("dist/dummy_dist-1.0-py3-none-any.whl") as wf:
        license_files = {
            "dummy_dist-1.0.dist-info/licenses/" + fname
            for fname in {"licenses_dir/DUMMYFILE", "LICENSE"}
        }
        assert set(wf.namelist()) == DEFAULT_FILES | license_files
        metadata = wf.read("dummy_dist-1.0.dist-info/METADATA").decode("utf8")
        assert "License-File: licenses_dir/DUMMYFILE" in metadata
        assert "License-File: LICENSE" in metadata

