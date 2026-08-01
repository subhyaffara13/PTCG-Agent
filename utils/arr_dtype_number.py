
def arr_dtype_number(arr, num):
    ''' Return dtype for given number of items per element'''
    return np.dtype(arr.dtype.str[:2] + str(num))

