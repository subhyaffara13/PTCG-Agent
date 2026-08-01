
def is_empty_block(block: BasicBlock) -> bool:
    return len(block.ops) == 1 and isinstance(block.ops[0], Unreachable)

