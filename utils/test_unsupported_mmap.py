
def test_unsupported_mmap():
    # Test containers that cannot be mapped to numpy types
    for filename in {'test-8000Hz-le-3ch-5S-24bit.wav',
                     'test-8000Hz-le-3ch-5S-36bit.wav',
                     'test-8000Hz-le-3ch-5S-45bit.wav',
                     'test-8000Hz-le-3ch-5S-53bit.wav',
                     'test-1234Hz-le-1ch-10S-20bit-extra.wav'}:
        with raises(ValueError, match="mmap.*not compatible"):
            rate, data = wavfile.read(datafile(filename), mmap=True)

