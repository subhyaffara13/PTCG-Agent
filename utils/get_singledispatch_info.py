
def get_singledispatch_info(typ: Instance) -> SingledispatchTypeVars | None:
    if len(typ.args) == 2:
        return SingledispatchTypeVars(*typ.args)  # type: ignore[arg-type]
    return None

