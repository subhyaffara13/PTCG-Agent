
def remove_na_arraylike(arr: Series | Index | np.ndarray):
    """
    Return array-like containing only true/non-NaN values, possibly empty.
    """
    if isinstance(arr.dtype, ExtensionDtype):
        return arr[notna(arr)]
    else:
        return arr[notna(np.asarray(arr))]

