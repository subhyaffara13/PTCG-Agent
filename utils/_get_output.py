
def _get_output(output, input, shape=None, complex_output=False):
    if shape is None:
        shape = input.shape
    if output is None:
        if not complex_output:
            output = np.zeros(shape, dtype=input.dtype.name)
        else:
            complex_type = np.promote_types(input.dtype, np.complex64)
            output = np.zeros(shape, dtype=complex_type)
    elif isinstance(output, type | np.dtype):
        # Classes (like `np.float32`) and dtypes are interpreted as dtype
        if complex_output and np.dtype(output).kind != 'c':
            warnings.warn("promoting specified output dtype to complex", stacklevel=3)
            output = np.promote_types(output, np.complex64)
        output = np.zeros(shape, dtype=output)
    elif isinstance(output, str):
        output = np.dtype(output)
        if complex_output and output.kind != 'c':
            raise RuntimeError("output must have complex dtype")
        elif not issubclass(output.type, np.number):
            raise RuntimeError("output must have numeric dtype")
        output = np.zeros(shape, dtype=output)
    else:
        # output was supplied as an array
        output = np.asarray(output)
        if output.shape != shape:
            raise RuntimeError("output shape not correct")
        elif complex_output and output.dtype.kind != 'c':
            raise RuntimeError("output must have complex dtype")
    return output

