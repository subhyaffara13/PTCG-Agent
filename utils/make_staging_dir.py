
def make_staging_dir(tmp_path):
    staging_dir = tmp_path / "staging"
    staging_dir.mkdir()
    return staging_dir

