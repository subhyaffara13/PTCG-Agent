
def test_build_number(dummy_dist, monkeypatch, tmp_path):
    monkeypatch.chdir(dummy_dist)
    bdist_wheel_cmd(bdist_dir=str(tmp_path), build_number="2").run()
    with ZipFile("dist/dummy_dist-1.0-2-py3-none-any.whl") as wf:
        filenames = set(wf.namelist())
        assert "dummy_dist-1.0.dist-info/RECORD" in filenames
        assert "dummy_dist-1.0.dist-info/METADATA" in filenames

