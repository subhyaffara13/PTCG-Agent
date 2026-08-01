
def pyarrow_string_dtype(request):
    """
    Parametrized fixture for string dtypes backed by Pyarrow.

    * 'str[pyarrow]'
    * 'string[pyarrow]'
    """
    return pd.StringDtype(*request.param)

