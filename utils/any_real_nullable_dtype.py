
def any_real_nullable_dtype(request):
    """
    Parameterized fixture for all real dtypes that can hold NA.

    * float
    * 'float32'
    * 'float64'
    * 'Float32'
    * 'Float64'
    * 'UInt8'
    * 'UInt16'
    * 'UInt32'
    * 'UInt64'
    * 'Int8'
    * 'Int16'
    * 'Int32'
    * 'Int64'
    * 'uint8[pyarrow]'
    * 'uint16[pyarrow]'
    * 'uint32[pyarrow]'
    * 'uint64[pyarrow]'
    * 'int8[pyarrow]'
    * 'int16[pyarrow]'
    * 'int32[pyarrow]'
    * 'int64[pyarrow]'
    * 'float[pyarrow]'
    * 'double[pyarrow]'
    """
    return request.param

