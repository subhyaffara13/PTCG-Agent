
def string_dtype_no_object(request):
    """
    Parametrized fixture for string dtypes.
    * 'string[python]' (NA variant)
    * 'string[pyarrow]' (NA variant)
    * 'str' (NaN variant, with pyarrow)
    * 'str' (NaN variant, without pyarrow)
    """
    # need to instantiate the StringDtype here instead of in the params
    # to avoid importing pyarrow during test collection
    storage, na_value = request.param
    return pd.StringDtype(storage, na_value)

