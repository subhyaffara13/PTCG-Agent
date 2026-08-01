
def test_licenses_deprecated(dummy_dist, monkeypatch, tmp_path):
    dummy_dist.joinpath("setup.cfg").write_text(
        "[metadata]\nlicense_file=licenses_dir/DUMMYFILE", encoding="utf-8"
    )
    monkeypatch.chdir(dummy_dist)

    bdist_wheel_cmd(bdist_dir=str(tmp_path)).run()

    with ZipFile("dist/dummy_dist-1.0-py3-none-any.whl") as wf:
        license_files = {"dummy_dist-1.0.dist-info/licenses/licenses_dir/DUMMYFILE"}
        assert set(wf.namelist()) == DEFAULT_FILES | license_files

