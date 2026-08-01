
def infer_class_variances(info: TypeInfo) -> bool:
    if not info.defn.type_args:
        return True
    tvs = info.defn.type_vars
    success = True
    for i, tv in enumerate(tvs):
        if isinstance(tv, TypeVarType) and tv.variance == VARIANCE_NOT_READY:
            if not infer_variance(info, i):
                success = False
    return success

