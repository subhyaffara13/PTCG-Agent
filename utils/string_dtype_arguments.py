
def string_dtype_arguments(request):
    """
    Parametrized fixture for StringDtype storage and na_value.

    * 'python' + pd.NA
    * 'pyarrow' + pd.NA
    * 'pyarrow' + np.nan
    """
    return request.param

