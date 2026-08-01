
def mark_block_mypy_only(block: Block) -> None:
    block.accept(MarkImportsMypyOnlyVisitor())

