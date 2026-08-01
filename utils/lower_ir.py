
def lower_ir(ir: FuncIR, options: CompilerOptions) -> None:
    builder = LowLevelIRBuilder(None, options)
    visitor = LoweringVisitor(builder)
    visitor.transform_blocks(ir.blocks)
    ir.blocks = builder.blocks

