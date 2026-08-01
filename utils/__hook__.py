
def __hook__():
    global NumpyArrayType, NumpyDType, NumpyUfuncType
    from numpy import ufunc as NumpyUfuncType
    from numpy import ndarray as NumpyArrayType
    from numpy import dtype as NumpyDType
    return True

