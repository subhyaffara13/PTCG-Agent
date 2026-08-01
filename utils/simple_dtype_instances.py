
def simple_dtype_instances():
    params = []
    for dtype_class in simple_dtypes:
        dt = dtype_class()
        params.append(pytest.param(dt, id=str(dt)))
        if dt.byteorder != "|":
            dt = dt.newbyteorder()
            params.append(pytest.param(dt, id=str(dt)))
    return params

