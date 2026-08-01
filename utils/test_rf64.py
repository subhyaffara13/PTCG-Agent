
def test_rf64():
    # Compare equivalent RF64 and RIFF files
    for rf64, riff in {('test-44100Hz-le-1ch-4bytes-rf64.wav',
                        'test-44100Hz-le-1ch-4bytes.wav'),
                       ('test-8000Hz-le-3ch-5S-24bit-rf64.wav',
                        'test-8000Hz-le-3ch-5S-24bit.wav')}:
        rate1, data1 = wavfile.read(datafile(rf64), mmap=False)
        rate2, data2 = wavfile.read(datafile(riff), mmap=False)
        assert_array_equal(rate1, rate2)
        assert_array_equal(data1, data2)

