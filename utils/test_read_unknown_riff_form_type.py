
def test_read_unknown_riff_form_type():
    # RIFF, but not WAVE form
    for mmap in [False, True]:
        filename = 'Transparent Busy.ani'
        with open(datafile(filename), 'rb') as fp:
            with raises(ValueError, match='Not a WAV file.*ACON'):
                wavfile.read(fp, mmap=mmap)

