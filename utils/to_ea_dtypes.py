
def to_ea_dtypes(dtypes):
    """convert list of string dtypes to EA dtype"""
    return [getattr(pd, dt + "Dtype") for dt in dtypes]

