
def add_block(
    decs: Decs, incs: Incs, cache: BlockCache, blocks: list[BasicBlock], label: BasicBlock
) -> BasicBlock:
    if not decs and not incs:
        return label

    # TODO: be able to share *partial* results
    if (label, decs, incs) in cache:
        return cache[label, decs, incs]

    block = BasicBlock()
    blocks.append(block)
    block.ops.extend(DecRef(reg, is_xdec=xdec) for reg, xdec in decs)
    block.ops.extend(IncRef(reg) for reg in incs)
    block.ops.append(Goto(label))
    cache[label, decs, incs] = block
    return block

