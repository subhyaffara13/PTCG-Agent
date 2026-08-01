
def process_conditional(
    self: IRBuilder, e: Expression, true: BasicBlock, false: BasicBlock
) -> None:
    if isinstance(e, OpExpr) and e.op in ["and", "or"]:
        if e.op == "and":
            # Short circuit 'and' in a conditional context.
            new = BasicBlock()
            process_conditional(self, e.left, new, false)
            self.activate_block(new)
            process_conditional(self, e.right, true, false)
        else:
            # Short circuit 'or' in a conditional context.
            new = BasicBlock()
            process_conditional(self, e.left, true, new)
            self.activate_block(new)
            process_conditional(self, e.right, true, false)
    elif isinstance(e, UnaryExpr) and e.op == "not":
        process_conditional(self, e.expr, false, true)
    else:
        res = maybe_process_conditional_comparison(self, e, true, false)
        if res:
            return
        # Catch-all for arbitrary expressions.
        reg = self.accept(e)
        self.add_bool_branch(reg, true, false)

