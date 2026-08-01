
def reference_data():
    # Matlab reference data
    MDATA = np.load(join(fftpack_test_dir, 'test.npz'))
    X = [MDATA[f'x{i}'] for i in range(MDATA_COUNT)]
    Y = [MDATA[f'y{i}'] for i in range(MDATA_COUNT)]

    # FFTW reference data: the data are organized as follows:
    #    * SIZES is an array containing all available sizes
    #    * for every type (1, 2, 3, 4) and every size, the array dct_type_size
    #    contains the output of the DCT applied to the input np.linspace(0, size-1,
    #    size)
    FFTWDATA_DOUBLE = np.load(join(fftpack_test_dir, 'fftw_double_ref.npz'))
    FFTWDATA_SINGLE = np.load(join(fftpack_test_dir, 'fftw_single_ref.npz'))
    FFTWDATA_SIZES = FFTWDATA_DOUBLE['sizes']
    assert len(FFTWDATA_SIZES) == FFTWDATA_COUNT

    if is_longdouble_binary_compatible():
        FFTWDATA_LONGDOUBLE = np.load(
            join(fftpack_test_dir, 'fftw_longdouble_ref.npz'))
    else:
        FFTWDATA_LONGDOUBLE = {k: v.astype(np.longdouble)
                               for k,v in FFTWDATA_DOUBLE.items()}

    ref = {
        'FFTWDATA_LONGDOUBLE': FFTWDATA_LONGDOUBLE,
        'FFTWDATA_DOUBLE': FFTWDATA_DOUBLE,
        'FFTWDATA_SINGLE': FFTWDATA_SINGLE,
        'FFTWDATA_SIZES': FFTWDATA_SIZES,
        'X': X,
        'Y': Y
    }

    yield ref

    if is_longdouble_binary_compatible():
        FFTWDATA_LONGDOUBLE.close()
    FFTWDATA_SINGLE.close()
    FFTWDATA_DOUBLE.close()
    MDATA.close()

