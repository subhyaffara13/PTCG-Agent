
def strip_target(node: MypyFile | FuncDef | OverloadedFuncDef) -> None:
    """Reset a fine-grained incremental target to state before semantic analysis.

    Args:
        node: node to strip
    """
    visitor = NodeStripVisitor()
    if isinstance(node, MypyFile):
        visitor.strip_file_top_level(node)
    else:
        node.accept(visitor)

