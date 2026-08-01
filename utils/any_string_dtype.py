
def any_string_dtype(request):
    """
    Parametrized fixture for string dtypes.
    * 'object'
    * 'string[python]' (NA variant)
    * 'string[pyarrow]' (NA variant)
    * 'str' (NaN variant, with pyarrow)
    * 'str' (NaN variant, without pyarrow)
    """
    if isinstance(request.param, np.dtype):
        return request.param
    else:
        # need to instantiate the StringDtype here instead of in the params
        # to avoid importing pyarrow during test collection
        storage, na_value = request.param
        return pd.StringDtype(storage, na_value)

