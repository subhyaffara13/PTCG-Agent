
def get_dtype(x: torch.Tensor | NumberType):
    if isinstance(x, torch.Tensor):
        return x.dtype
    else:
        return type_to_dtype(type(x))


def get_dtype(obj) -> DtypeObj:
    if isinstance(obj, DataFrame):
        # Note: we are assuming only one column
        return obj.dtypes.iat[0]
    else:
        return obj.dtype


def get_dtype(dtype, coerce_int=None):
    if coerce_int is False and "int" in dtype:
        return None
    return pandas_dtype(dtype)


def get_dtype(na_object, coerce=True):
    """Helper to work around pd_NA boolean behavior"""
    # explicit is check for pd_NA because != with pd_NA returns pd_NA
    if na_object is pd_NA or na_object != "unset":
        return np.dtypes.StringDType(na_object=na_object, coerce=coerce)
    else:
        return np.dtypes.StringDType(coerce=coerce)

