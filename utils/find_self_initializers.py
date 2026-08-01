
def find_self_initializers(fdef: FuncBase) -> list[tuple[str, Expression, Type | None]]:
    """Find attribute initializers in a method.

    Return a list of pairs (attribute name, r.h.s. expression).
    """
    traverser = SelfTraverser()
    fdef.accept(traverser)
    return traverser.results

