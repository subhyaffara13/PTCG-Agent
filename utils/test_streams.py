
def test_streams():
    for filename in ['test-44100Hz-le-1ch-4bytes.wav',
                     'test-8000Hz-le-2ch-1byteu.wav',
                     'test-44100Hz-2ch-32bit-float-le.wav',
                     'test-44100Hz-2ch-32bit-float-be.wav',
                     'test-8000Hz-le-5ch-9S-5bit.wav',
                     'test-8000Hz-le-4ch-9S-12bit.wav',
                     'test-8000Hz-le-3ch-5S-24bit.wav',
                     'test-1234Hz-le-1ch-10S-20bit-extra.wav',
                     'test-8000Hz-le-3ch-5S-36bit.wav',
                     'test-8000Hz-le-3ch-5S-45bit.wav',
                     'test-8000Hz-le-3ch-5S-53bit.wav',
                     'test-8000Hz-le-3ch-5S-64bit.wav',
                     'test-44100Hz-be-1ch-4bytes.wav', # RIFX
                     'test-44100Hz-le-1ch-4bytes-rf64.wav']:
        dfname = datafile(filename)
        with open(dfname, 'rb') as fp1, open(dfname, 'rb') as fp2:
            rate1, data1 = wavfile.read(fp1)
            rate2, data2 = wavfile.read(Nonseekable(fp2))
            rate3, data3 = wavfile.read(dfname, mmap=False)
            assert_equal(rate1, rate3)
            assert_equal(rate2, rate3)
            assert_equal(data1, data3)
            assert_equal(data2, data3)

