
def _get_first_fqn(
    const_attrs: ConstantAttrMap,
    key: _ConstantAttributeType,
) -> Any:
    fqns = const_attrs.get(key)
    return fqns[0] if fqns else None

