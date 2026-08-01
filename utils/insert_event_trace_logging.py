
def insert_event_trace_logging(fn: FuncIR, options: CompilerOptions) -> None:
    builder = LowLevelIRBuilder(None, options)
    transform = LogTraceEventTransform(builder, fn.decl.fullname)
    transform.transform_blocks(fn.blocks)
    fn.blocks = builder.blocks

