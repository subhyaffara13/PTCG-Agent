
def test_read_unknown_filetype_fail():
    # Not an RIFF
    for mmap in [False, True]:
        filename = 'example_1.nc'
        with open(datafile(filename), 'rb') as fp:
            with raises(ValueError, match="CDF.*'RIFF', 'RIFX', and 'RF64' supported"):
                wavfile.read(fp, mmap=mmap)

