
def test_read_incomplete_chunk():
    # File ends inside 'fmt ' chunk ID, no data read
    for mmap in [False, True]:
        filename = 'test-44100Hz-le-1ch-4bytes-incomplete-chunk.wav'
        with open(datafile(filename), 'rb') as fp:
            with raises(ValueError, match="Incomplete chunk ID.*b'f'"):
                wavfile.read(fp, mmap=mmap)

