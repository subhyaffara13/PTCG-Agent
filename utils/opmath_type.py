
def opmath_type(scalar_t: BaseCppType) -> BaseCppType:
    if scalar_t == api_types.scalar_t:
        return api_types.opmath_t
    raise NotImplementedError

