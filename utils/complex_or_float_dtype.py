
def complex_or_float_dtype(request):
    """
    Parameterized fixture for complex and numpy float dtypes.

    * complex
    * 'complex64'
    * 'complex128'
    * float
    * 'float32'
    * 'float64'
    """
    return request.param

