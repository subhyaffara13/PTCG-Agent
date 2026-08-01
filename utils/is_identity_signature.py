
def is_identity_signature(sig: Type) -> bool:
    """Is type a callable of form T -> T (where T is a type variable)?"""
    sig = get_proper_type(sig)
    if isinstance(sig, CallableType) and sig.arg_kinds == [ARG_POS]:
        if isinstance(sig.arg_types[0], TypeVarType) and isinstance(sig.ret_type, TypeVarType):
            return sig.arg_types[0].id == sig.ret_type.id
    return False

