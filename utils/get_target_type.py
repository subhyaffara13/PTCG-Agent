from typing import Callable

def get_target_type(
    tvar: TypeVarLikeType,
    type: Type,
    callable: CallableType,
    report_incompatible_typevar_value: Callable[[CallableType, Type, str, Context], None],
    context: Context,
    skip_unsatisfied: bool,
    id_to_type: dict[TypeVarId, Type],
) -> Type | None:
    p_type = get_proper_type(type)
    if isinstance(p_type, UninhabitedType) and p_type.ambiguous and tvar.has_default():
        # Gradually expand defaults, as they may depend on previous type variables.
        return expand_type(tvar.default, id_to_type)
    if isinstance(tvar, ParamSpecType):
        return type
    if isinstance(tvar, TypeVarTupleType):
        return type
    assert isinstance(tvar, TypeVarType)
    values = tvar.values
    if values:
        if isinstance(p_type, AnyType):
            return type
        if isinstance(p_type, TypeVarType) and p_type.values:
            # Allow substituting T1 for T if every allowed value of T1
            # is also a legal value of T.
            if all(any(mypy.subtypes.is_same_type(v, v1) for v in values) for v1 in p_type.values):
                return type
        matching = []
        for value in values:
            if mypy.subtypes.is_subtype(type, value):
                matching.append(value)
        if matching:
            best = matching[0]
            # If there are more than one matching value, we select the narrowest
            for match in matching[1:]:
                if mypy.subtypes.is_subtype(match, best):
                    best = match
            return best
        if skip_unsatisfied:
            return None
        report_incompatible_typevar_value(callable, type, tvar.name, context)
    else:
        upper_bound = tvar.upper_bound
        if tvar.name == "Self":
            # Internally constructed Self-types contain class type variables in upper bound,
            # so we need to erase them to avoid false positives. This is safe because we do
            # not support type variables in upper bounds of user defined types.
            upper_bound = erase_typevars(upper_bound)
        if not mypy.subtypes.is_subtype(type, upper_bound):
            if skip_unsatisfied:
                return None
            report_incompatible_typevar_value(callable, type, tvar.name, context)
    return type

