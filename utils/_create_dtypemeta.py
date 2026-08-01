
def _create_dtypemeta(scalar_type):
    if NumpyDType is True: __hook__() # a bit hacky I think
    if scalar_type is None:
        return NumpyDType
    return type(NumpyDType(scalar_type))

