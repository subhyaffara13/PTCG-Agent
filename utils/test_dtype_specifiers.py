
def test_dtype_specifiers():
    # Numpy 1.7.0-dev had a bug where 'i2' wouldn't work.
    # Specifying np.int16 or similar only works from the same commit as this
    # comment was made.
    with make_simple(BytesIO(), mode='w') as f:
        f.createDimension('x',4)
        f.createVariable('v1', 'i2', ['x'])
        f.createVariable('v2', np.int16, ['x'])
        f.createVariable('v3', np.dtype(np.int16), ['x'])

