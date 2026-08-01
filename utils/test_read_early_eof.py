
def test_read_early_eof():
    # File ends after 'fact' chunk at boundary, no data read
    for mmap in [False, True]:
        filename = 'test-44100Hz-le-1ch-4bytes-early-eof-no-data.wav'
        with open(datafile(filename), 'rb') as fp:
            with raises(ValueError, match="Unexpected end of file."):
                wavfile.read(fp, mmap=mmap)

