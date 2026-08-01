
def vr_is_bool(vr: ValueRanges[_T]) -> TypeGuard[ValueRanges[SympyBoolean]]:
    return vr.is_bool

