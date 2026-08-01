
def _extremum_fill_value(obj, extremum, extremum_name):

    def _scalar_fill_value(dtype):
        try:
            return extremum[dtype.type]
        except KeyError as e:
            raise TypeError(
                f"Unsuitable type {dtype} for calculating {extremum_name}."
            ) from None

    dtype = _get_dtype_of(obj)
    return _recursive_fill_value(dtype, _scalar_fill_value)

