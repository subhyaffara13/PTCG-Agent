
def test_read_files(tmp_path, monkeypatch):
    dir_ = tmp_path / "dir_"
    (tmp_path / "_dir").mkdir(exist_ok=True)
    (tmp_path / "a.txt").touch()
    files = {"a.txt": "a", "dir1/b.txt": "b", "dir1/dir2/c.txt": "c"}
    write_files(files, dir_)

    secrets = Path(str(dir_) + "secrets")
    secrets.mkdir(exist_ok=True)
    write_files({"secrets.txt": "secret keys"}, secrets)

    with monkeypatch.context() as m:
        m.chdir(dir_)
        assert expand.read_files(list(files)) == "a\nb\nc"

        cannot_access_msg = r"Cannot access '.*\.\..a\.txt'"
        with pytest.raises(DistutilsOptionError, match=cannot_access_msg):
            expand.read_files(["../a.txt"])

        cannot_access_secrets_msg = r"Cannot access '.*secrets\.txt'"
        with pytest.raises(DistutilsOptionError, match=cannot_access_secrets_msg):
            expand.read_files(["../dir_secrets/secrets.txt"])

    # Make sure the same APIs work outside cwd
    assert expand.read_files(list(files), dir_) == "a\nb\nc"
    with pytest.raises(DistutilsOptionError, match=cannot_access_msg):
        expand.read_files(["../a.txt"], dir_)

