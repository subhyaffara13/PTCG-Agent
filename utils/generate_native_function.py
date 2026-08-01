
def generate_native_function(
    fn: FuncIR, emitter: Emitter, source_path: str, module_name: str
) -> None:
    declarations = Emitter(emitter.context)
    names = generate_names_for_ir(fn.arg_regs, fn.blocks)
    body = Emitter(emitter.context, names)
    visitor = FunctionEmitterVisitor(body, declarations, source_path, module_name)

    declarations.emit_line(f"{native_function_header(fn.decl, emitter)} {{")
    body.indent()

    for r in all_values(fn.arg_regs, fn.blocks):
        if isinstance(r.type, RTuple):
            emitter.declare_tuple_struct(r.type)
        if isinstance(r.type, RArray):
            continue  # Special: declared on first assignment

        if r in fn.arg_regs:
            continue  # Skip the arguments

        ctype = emitter.ctype_spaced(r.type)
        init = ""
        declarations.emit_line(
            "{ctype}{prefix}{name}{init};".format(
                ctype=ctype, prefix=REG_PREFIX, name=names[r], init=init
            )
        )

    # Before we emit the blocks, give them all labels
    blocks = fn.blocks
    for i, block in enumerate(blocks):
        block.label = i

    # Find blocks that are never jumped to or are only jumped to from the
    # block directly above it. This allows for more labels and gotos to be
    # eliminated during code generation.
    for block in fn.blocks:
        terminator = block.terminator
        assert isinstance(terminator, ControlOp), terminator

        for target in terminator.targets():
            is_next_block = target.label == block.label + 1

            # Always emit labels for GetAttr error checks since the emit code that
            # generates them will add instructions between the branch and the
            # next label, causing the label to be wrongly removed. A better
            # solution would be to change the IR so that it adds a basic block
            # in between the calls.
            is_problematic_op = isinstance(terminator, Branch) and any(
                isinstance(s, GetAttr) for s in terminator.sources()
            )

            if not is_next_block or is_problematic_op:
                fn.blocks[target.label].referenced = True

    common = frequently_executed_blocks(fn.blocks[0])

    for i in range(len(blocks)):
        block = blocks[i]
        visitor.rare = block not in common
        next_block = None
        if i + 1 < len(blocks):
            next_block = blocks[i + 1]
        body.emit_label(block)
        visitor.next_block = next_block

        ops = block.ops
        visitor.ops = ops
        visitor.op_index = 0
        while visitor.op_index < len(ops):
            ops[visitor.op_index].accept(visitor)
            visitor.op_index += 1

    body.emit_line("}")

    emitter.emit_from_emitter(declarations)
    emitter.emit_from_emitter(body)

