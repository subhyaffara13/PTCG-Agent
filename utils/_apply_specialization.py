
def _apply_specialization(
    builder: IRBuilder, expr: CallExpr, callee: RefExpr, name: str | None, typ: RType | None = None
) -> Value | None:
    # TODO: Allow special cases to have default args or named args. Currently they don't since
    #       they check that everything in arg_kinds is ARG_POS.

    # If there is a specializer for this function, try calling it.
    # Return the first successful one.
    if name and (name, typ) in specializers:
        for specializer in specializers[name, typ]:
            val = specializer(builder, expr, callee)
            if val is not None:
                return val
    return None

