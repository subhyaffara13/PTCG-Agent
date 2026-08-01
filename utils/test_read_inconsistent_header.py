
def test_read_inconsistent_header():
    # File header's size fields contradict each other
    for mmap in [False, True]:
        filename = 'test-8000Hz-le-3ch-5S-24bit-inconsistent.wav'
        with open(datafile(filename), 'rb') as fp:
            with raises(ValueError, match="header is invalid"):
                wavfile.read(fp, mmap=mmap)

