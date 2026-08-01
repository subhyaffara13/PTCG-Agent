
def dtype2(string_dtype_arguments2):
    storage, na_value = string_dtype_arguments2
    return pd.StringDtype(storage=storage, na_value=na_value)


def dtype2(na_object2, coerce2):
    """Second copy of the dtype fixture for tests that need two instances"""
    # explicit is check for pd_NA because != with pd_NA returns pd_NA
    if na_object2 is pd_NA or na_object2 != "unset":
        return StringDType(na_object=na_object2, coerce=coerce2)
    else:
        return StringDType(coerce=coerce2)

