
def format_blocks(
    blocks: list[BasicBlock],
    names: dict[Value, str],
    source_to_error: dict[ErrorSource, list[str]],
) -> list[str]:
    """Format a list of IR basic blocks into a human-readable form."""
    # First label all of the blocks
    for i, block in enumerate(blocks):
        block.label = i

    handler_map: dict[BasicBlock, list[BasicBlock]] = {}
    for b in blocks:
        if b.error_handler:
            handler_map.setdefault(b.error_handler, []).append(b)

    visitor = IRPrettyPrintVisitor(names)

    lines = []
    for i, block in enumerate(blocks):
        handler_msg = ""
        if block in handler_map:
            labels = sorted("L%d" % b.label for b in handler_map[block])
            handler_msg = " (handler for {})".format(", ".join(labels))

        lines.append("L%d:%s" % (block.label, handler_msg))
        if block in source_to_error:
            for error in source_to_error[block]:
                lines.append(f"  ERROR: {error}")
        ops = block.ops
        if (
            isinstance(ops[-1], Goto)
            and i + 1 < len(blocks)
            and ops[-1].label == blocks[i + 1]
            and not source_to_error.get(ops[-1], [])
        ):
            # Hide the last goto if it just goes to the next basic block,
            # and there are no assocatiated errors with the op.
            ops = ops[:-1]
        for op in ops:
            line = "    " + op.accept(visitor)
            lines.append(line)
            if op in source_to_error:
                first = len(lines) - 1
                # Use emojis to highlight the error
                for error in source_to_error[op]:
                    lines.append(f"    \U0001f446 ERROR: {error}")
                lines[first] = " \U0000274c " + lines[first][4:]

        if not isinstance(block.ops[-1], (Goto, Branch, Return, Unreachable)):
            # Each basic block needs to exit somewhere.
            lines.append("    [MISSING BLOCK EXIT OPCODE]")
    return lines

