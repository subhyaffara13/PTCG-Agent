
def remove_na(vector):
    """Helper method for removing null values from data vectors.

    Parameters
    ----------
    vector : vector object
        Must implement boolean masking with [] subscript syntax.

    Returns
    -------
    clean_clean : same type as ``vector``
        Vector of data with null values removed. May be a copy or a view.

    """
    return vector[pd.notnull(vector)]

