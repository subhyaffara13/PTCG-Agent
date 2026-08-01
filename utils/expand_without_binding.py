
def expand_without_binding(
    typ: Type, var: Var, itype: Instance, original_itype: Instance, mx: MemberContext
) -> Type:
    if not mx.preserve_type_var_ids:
        typ = freshen_all_functions_type_vars(typ)
    typ = expand_self_type_if_needed(typ, mx, var, original_itype)
    expanded = expand_type_by_instance(typ, itype)
    freeze_all_type_vars(expanded)
    return expanded

