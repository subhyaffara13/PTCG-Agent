
def arr_to_2d(arr, oned_as='row'):
    ''' Make ``arr`` exactly two dimensional

    If `arr` has more than 2 dimensions, raise a ValueError

    Parameters
    ----------
    arr : array
    oned_as : {'row', 'column'}, optional
       Whether to reshape 1-D vectors as row vectors or column vectors.
       See documentation for ``matdims`` for more detail

    Returns
    -------
    arr2d : array
       2-D version of the array
    '''
    dims = matdims(arr, oned_as)
    if len(dims) > 2:
        raise ValueError('Matlab 4 files cannot save arrays with more than '
                         '2 dimensions')
    return arr.reshape(dims)

