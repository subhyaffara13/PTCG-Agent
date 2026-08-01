
def test_glob_relative(tmp_path, monkeypatch):
    files = {
        "dir1/dir2/dir3/file1.txt",
        "dir1/dir2/file2.txt",
        "dir1/file3.txt",
        "a.ini",
        "b.ini",
        "dir1/c.ini",
        "dir1/dir2/a.ini",
    }

    write_files({k: "" for k in files}, tmp_path)
    patterns = ["**/*.txt", "[ab].*", "**/[ac].ini"]
    monkeypatch.chdir(tmp_path)
    assert set(expand.glob_relative(patterns)) == files
    # Make sure the same APIs work outside cwd
    assert set(expand.glob_relative(patterns, tmp_path)) == files

