
def test_dist_info_provided(dummy_dist, monkeypatch, tmp_path):
    monkeypatch.chdir(dummy_dist)
    distinfo = tmp_path / "dummy_dist.dist-info"

    distinfo.mkdir()
    (distinfo / "METADATA").write_text("name: helloworld", encoding="utf-8")

    # We don't control the metadata. According to PEP-517, "The hook MAY also
    # create other files inside this directory, and a build frontend MUST
    # preserve".
    (distinfo / "FOO").write_text("bar", encoding="utf-8")

    bdist_wheel_cmd(bdist_dir=str(tmp_path), dist_info_dir=str(distinfo)).run()
    expected = {
        "dummy_dist-1.0.dist-info/FOO",
        "dummy_dist-1.0.dist-info/RECORD",
    }
    with ZipFile("dist/dummy_dist-1.0-py3-none-any.whl") as wf:
        files_found = set(wf.namelist())
    # Check that all expected files are there.
    assert expected - files_found == set()
    # Make sure there is no accidental egg-info bleeding into the wheel.
    assert not [path for path in files_found if 'egg-info' in str(path)]

