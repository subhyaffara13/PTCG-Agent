
def test_matfile_version(version, filt, regex):
    use_filt = pjoin(test_data_path, f'test*{filt}.mat')
    files = glob(use_filt)
    if regex is not None:
        files = [file for file in files if re.match(regex, file) is not None]
    assert len(files) > 0, \
        f"No files for version {version} using filter {filt}"
    for file in files:
        got_version = matfile_version(file)
        assert got_version[0] == version

