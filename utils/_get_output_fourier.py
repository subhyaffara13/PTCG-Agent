
def _get_output_fourier(output, input):
    if output is None:
        if input.dtype.type in [np.complex64, np.complex128, np.float32]:
            output = np.zeros(input.shape, dtype=input.dtype)
        else:
            output = np.zeros(input.shape, dtype=np.float64)
    elif type(output) is type:
        if output not in [np.complex64, np.complex128,
                          np.float32, np.float64]:
            raise RuntimeError("output type not supported")
        output = np.zeros(input.shape, dtype=output)
    elif output.shape != input.shape:
        raise RuntimeError("output shape not correct")
    return output

