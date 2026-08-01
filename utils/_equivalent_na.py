
def _equivalent_na(dtype, null):
    if dtype.na_value is pd.NA and null is pd.NA:
        return True
    elif _isnan(dtype.na_value) and _isnan(null):
        return True
    else:
        return False

