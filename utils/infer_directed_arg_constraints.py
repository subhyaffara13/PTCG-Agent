
def infer_directed_arg_constraints(left: Type, right: Type, direction: int) -> list[Constraint]:
    """Infer constraints between two arguments using direction between original callables."""
    if isinstance(left, (ParamSpecType, UnpackType)) or isinstance(
        right, (ParamSpecType, UnpackType)
    ):
        # This avoids bogus constraints like T <: P.args
        # TODO: can we infer something useful for *T vs P?
        return []
    if direction == SUBTYPE_OF:
        # We invert direction to account for argument contravariance.
        return infer_constraints(left, right, neg_op(direction))
    else:
        return infer_constraints(right, left, neg_op(direction))

