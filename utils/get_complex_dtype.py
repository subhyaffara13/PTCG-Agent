
def get_complex_dtype(dtype):
    return {single: csingle, double: cdouble,
            csingle: csingle, cdouble: cdouble}[dtype]

