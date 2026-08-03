import time

def check_simple(ncfileobj):
    '''Example fileobj tests '''
    assert_equal(ncfileobj.history, b'Created for a test')
    time = ncfileobj.variables['time']
    assert_equal(time.units, b'days since 2008-01-01')
    assert_equal(time.shape, (N_EG_ELS,))
    assert_equal(time[-1], N_EG_ELS-1)

