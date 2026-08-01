
def test_licenses_default(dummy_dist, monkeypatch, tmp_path):
    monkeypatch.chdir(dummy_dist)
    bdist_wheel_cmd(bdist_dir=str(tmp_path)).run()
    with ZipFile("dist/dummy_dist-1.0-py3-none-any.whl") as wf:
        license_files = {
            "dummy_dist-1.0.dist-info/licenses/" + fname
            for fname in DEFAULT_LICENSE_FILES
        }
        assert set(wf.namelist()) == DEFAULT_FILES | license_files

