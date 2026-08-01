
def test_sanity_check_setuptools_own_sdist(setuptools_sdist):
    with tarfile.open(setuptools_sdist) as tar:
        files = tar.getnames()

    # setuptools sdist should not include the .tox folder
    tox_files = [name for name in files if ".tox" in name]
    assert len(tox_files) == 0, f"not empty {tox_files}"

