
def any_numeric_ea_and_arrow_dtype(request):
    """
    Parameterized fixture for any nullable integer dtype and
    any float ea dtypes.

    * 'UInt8'
    * 'Int8'
    * 'UInt16'
    * 'Int16'
    * 'UInt32'
    * 'Int32'
    * 'UInt64'
    * 'Int64'
    * 'Float32'
    * 'Float64'
    * 'uint8[pyarrow]'
    * 'int8[pyarrow]'
    * 'uint16[pyarrow]'
    * 'int16[pyarrow]'
    * 'uint32[pyarrow]'
    * 'int32[pyarrow]'
    * 'uint64[pyarrow]'
    * 'int64[pyarrow]'
    * 'float32[pyarrow]'
    * 'float64[pyarrow]'
    """
    return request.param

