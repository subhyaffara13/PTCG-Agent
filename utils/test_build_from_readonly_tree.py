import os

def test_build_from_readonly_tree(dummy_dist, monkeypatch, tmp_path):
    basedir = str(tmp_path.joinpath("dummy"))
    shutil.copytree(str(dummy_dist), basedir)
    monkeypatch.chdir(basedir)

    # Make the tree read-only
    for root, _dirs, files in os.walk(basedir):
        for fname in files:
            os.chmod(os.path.join(root, fname), stat.S_IREAD)

    bdist_wheel_cmd().run()

