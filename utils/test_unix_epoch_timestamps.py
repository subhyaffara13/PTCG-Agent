
def test_unix_epoch_timestamps(dummy_dist, monkeypatch, tmp_path):
    monkeypatch.setenv("SOURCE_DATE_EPOCH", "0")
    monkeypatch.chdir(dummy_dist)
    bdist_wheel_cmd(bdist_dir=str(tmp_path), build_number="2a").run()
    with ZipFile("dist/dummy_dist-1.0-2a-py3-none-any.whl") as wf:
        for zinfo in wf.filelist:
            assert zinfo.date_time >= (1980, 1, 1, 0, 0, 0)  # min epoch is used

