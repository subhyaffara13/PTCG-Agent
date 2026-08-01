
def test_read_unknown_wave_format():
    # RIFF and WAVE, but not supported format
    for mmap in [False, True]:
        filename = 'test-8000Hz-le-1ch-1byte-ulaw.wav'
        with open(datafile(filename), 'rb') as fp:
            with raises(ValueError, match='Unknown wave file format.*MULAW.*'
                        'Supported formats'):
                wavfile.read(fp, mmap=mmap)

