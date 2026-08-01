
def compare_tagged(self: LowLevelIRBuilder, lhs: Value, rhs: Value, op: str, line: int) -> Value:
    """Compare two tagged integers using given operator (value context)."""
    # generate fast binary logic ops on short ints
    if (is_short_int_rprimitive(lhs.type) or is_short_int_rprimitive(rhs.type)) and op in (
        "==",
        "!=",
    ):
        quick = True
    else:
        quick = is_short_int_rprimitive(lhs.type) and is_short_int_rprimitive(rhs.type)
    if quick:
        return self.comparison_op(lhs, rhs, int_comparison_op_mapping[op][0], line)
    op_type, c_func_desc, negate_result, swap_op = int_comparison_op_mapping[op]
    result = Register(bool_rprimitive)
    short_int_block, int_block, out = BasicBlock(), BasicBlock(), BasicBlock()
    check_lhs = self.check_tagged_short_int(lhs, line, negated=True)
    if op in ("==", "!="):
        self.add(Branch(check_lhs, int_block, short_int_block, Branch.BOOL))
    else:
        # for non-equality logical ops (less/greater than, etc.), need to check both sides
        short_lhs = BasicBlock()
        self.add(Branch(check_lhs, int_block, short_lhs, Branch.BOOL))
        self.activate_block(short_lhs)
        check_rhs = self.check_tagged_short_int(rhs, line, negated=True)
        self.add(Branch(check_rhs, int_block, short_int_block, Branch.BOOL))
    self.activate_block(int_block)
    if swap_op:
        args = [rhs, lhs]
    else:
        args = [lhs, rhs]
    call = self.call_c(c_func_desc, args, line)
    if negate_result:
        # TODO: introduce UnaryIntOp?
        call_result = self.unary_op(call, "not", line)
    else:
        call_result = call
    self.add(Assign(result, call_result, line))
    self.goto(out)
    self.activate_block(short_int_block)
    eq = self.comparison_op(lhs, rhs, op_type, line)
    self.add(Assign(result, eq, line))
    self.goto_and_activate(out)
    return result

