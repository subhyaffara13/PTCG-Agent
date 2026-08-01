
def set_callable_name(sig: Type, fdef: FuncDef) -> ProperType:
    sig = get_proper_type(sig)
    if isinstance(sig, FunctionLike):
        if fdef.info:
            if fdef.info.fullname in TPDICT_FB_NAMES:
                # Avoid exposing the internal _TypedDict name.
                class_name = "TypedDict"
            else:
                class_name = fdef.info.name
            return sig.with_name(f"{fdef.name} of {class_name}")
        else:
            return sig.with_name(fdef.name)
    else:
        return sig

