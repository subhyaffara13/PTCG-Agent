
def is_bool_expr(constraint: object) -> bool:
    if isinstance(constraint, BinConstraintD):
        return constraint.op in [op_gt, op_lt, op_neq, op_eq]
    else:
        return isinstance(constraint, (BVar, Conj, Disj))

