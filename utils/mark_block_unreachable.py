
def mark_block_unreachable(block: Block) -> None:
    block.is_unreachable = True
    block.accept(MarkImportsUnreachableVisitor())

