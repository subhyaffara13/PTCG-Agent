
def test_licenses_disabled(dummy_dist, monkeypatch, tmp_path):
    dummy_dist.joinpath("setup.cfg").write_text(
        "[metadata]\nlicense_files=\n", encoding="utf-8"
    )
    monkeypatch.chdir(dummy_dist)
    bdist_wheel_cmd(bdist_dir=str(tmp_path)).run()
    with ZipFile("dist/dummy_dist-1.0-py3-none-any.whl") as wf:
        assert set(wf.namelist()) == DEFAULT_FILES

