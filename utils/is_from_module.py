
def is_from_module(node: SymbolNode, module: MypyFile) -> bool:
    return node.fullname == module.fullname + "." + node.name

