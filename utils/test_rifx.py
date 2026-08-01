
def test_rifx():
    # Compare equivalent RIFX and RIFF files
    for rifx, riff in {('test-44100Hz-be-1ch-4bytes.wav',
                        'test-44100Hz-le-1ch-4bytes.wav'),
                       ('test-8000Hz-be-3ch-5S-24bit.wav',
                        'test-8000Hz-le-3ch-5S-24bit.wav')}:
        rate1, data1 = wavfile.read(datafile(rifx), mmap=False)
        rate2, data2 = wavfile.read(datafile(riff), mmap=False)
        assert_equal(rate1, rate2)
        assert_equal(data1, data2)

