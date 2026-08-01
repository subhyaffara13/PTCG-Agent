
def cleanup_cfg(blocks: list[BasicBlock]) -> None:
    """Cleanup the control flow graph.

    This eliminates obviously dead basic blocks and eliminates blocks that contain
    nothing but a single jump.

    There is a lot more that could be done.
    """
    changed = True
    while changed:
        # First collapse any jumps to basic block that only contain a goto
        for block in blocks:
            for i, tgt in enumerate(block.terminator.targets()):
                block.terminator.set_target(i, get_real_target(tgt))

        # Then delete any blocks that have no predecessors
        changed = False
        cfg = get_cfg(blocks)
        orig_blocks = blocks.copy()
        blocks.clear()
        for i, block in enumerate(orig_blocks):
            if i == 0 or cfg.pred[block]:
                blocks.append(block)
            else:
                changed = True

