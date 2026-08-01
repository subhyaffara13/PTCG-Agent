
def fftw_dct_ref(type, size, dt):
    x = np.linspace(0, size-1, size).astype(dt)
    dt = np.result_type(np.float32, dt)
    if dt == np.float64:
        data = FFTWDATA_DOUBLE
    elif dt == np.float32:
        data = FFTWDATA_SINGLE
    else:
        raise ValueError()
    y = (data[f'dct_{type}_{size}']).astype(dt)
    return x, y, dt


def fftw_dct_ref(type, size, dt, reference_data):
    x = np.linspace(0, size-1, size).astype(dt)
    dt = np.result_type(np.float32, dt)
    if dt == np.float64:
        data = reference_data['FFTWDATA_DOUBLE']
    elif dt == np.float32:
        data = reference_data['FFTWDATA_SINGLE']
    elif dt == np.longdouble:
        data = reference_data['FFTWDATA_LONGDOUBLE']
    else:
        raise ValueError()
    y = (data[f'dct_{type}_{size}']).astype(dt)
    return x, y, dt

