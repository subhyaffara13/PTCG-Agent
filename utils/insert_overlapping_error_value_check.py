
def insert_overlapping_error_value_check(ops: list[Op], target: Value) -> ComparisonOp:
    """Append to ops to check for an overlapping error value."""
    typ = target.type
    if isinstance(typ, RTuple):
        item = TupleGet(target, 0)
        ops.append(item)
        return insert_overlapping_error_value_check(ops, item)
    else:
        errvalue: Value
        if is_float_rprimitive(target.type):
            errvalue = Float(float(typ.c_undefined))
        else:
            errvalue = Integer(int(typ.c_undefined), rtype=typ)
        op = ComparisonOp(target, errvalue, ComparisonOp.EQ)
        ops.append(op)
        return op

