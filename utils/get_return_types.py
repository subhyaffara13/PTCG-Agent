
def get_return_types(typemap: dict[Expression, Type], func: FuncDef) -> list[Type]:
    """Find all the types returned by return statements in func."""
    finder = ReturnFinder(typemap)
    func.body.accept(finder)
    return finder.return_types

