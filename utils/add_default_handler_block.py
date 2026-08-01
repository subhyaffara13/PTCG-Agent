
def add_default_handler_block(ir: FuncIR) -> BasicBlock:
    block = BasicBlock()
    ir.blocks.append(block)
    op = LoadErrorValue(ir.ret_type)
    block.ops.append(op)
    block.ops.append(Return(op))
    return block

