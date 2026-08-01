
def maybe_process_conditional_comparison(
    self: IRBuilder, e: Expression, true: BasicBlock, false: BasicBlock
) -> bool:
    """Transform simple tagged integer comparisons in a conditional context.

    Return True if the operation is supported (and was transformed). Otherwise,
    do nothing and return False.

    Args:
        self: IR form Builder
        e: Arbitrary expression
        true: Branch target if comparison is true
        false: Branch target if comparison is false
    """
    if not isinstance(e, ComparisonExpr) or len(e.operands) != 2:
        return False
    ltype = self.node_type(e.operands[0])
    rtype = self.node_type(e.operands[1])
    if not (
        (is_tagged(ltype) or is_fixed_width_rtype(ltype))
        and (is_tagged(rtype) or is_fixed_width_rtype(rtype))
    ):
        return False
    op = e.operators[0]
    if op not in ("==", "!=", "<", "<=", ">", ">="):
        return False
    left_expr = e.operands[0]
    right_expr = e.operands[1]
    borrow_left = is_borrow_friendly_expr(self, right_expr)
    left = self.accept(left_expr, can_borrow=borrow_left)
    right = self.accept(right_expr, can_borrow=True)
    if is_fixed_width_rtype(ltype) or is_fixed_width_rtype(rtype):
        if not is_fixed_width_rtype(ltype):
            left = self.coerce(left, rtype, e.line)
        elif not is_fixed_width_rtype(rtype):
            right = self.coerce(right, ltype, e.line)
        reg = self.binary_op(left, right, op, e.line)
        self.builder.flush_keep_alives(e.line)
        self.add_bool_branch(reg, true, false)
    else:
        # "left op right" for two tagged integers
        reg = self.builder.binary_op(left, right, op, e.line)
        self.flush_keep_alives(e.line)
        self.add_bool_branch(reg, true, false)
    return True

