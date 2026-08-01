
def is_comprehension(node: nodes.NodeNG) -> bool:
    comprehensions = (
        nodes.ListComp,
        nodes.SetComp,
        nodes.DictComp,
        nodes.GeneratorExp,
    )
    return isinstance(node, comprehensions)

