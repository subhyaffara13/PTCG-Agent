
def test_read_early_eof_with_data():
    # File ends inside 'data' chunk, but we keep incomplete data
    for mmap in [False, True]:
        filename = 'test-44100Hz-le-1ch-4bytes-early-eof.wav'
        with open(datafile(filename), 'rb') as fp:
            with warns(wavfile.WavFileWarning, match='Reached EOF'):
                rate, data = wavfile.read(fp, mmap=mmap)
                assert data.size > 0
                assert rate == 44100
                # also test writing (gh-12176)
                data[0] = 0

