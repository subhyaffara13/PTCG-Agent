
def rename_refs(names: list[NameExpr], index: int) -> None:
    name = names[0].name
    new_name = name + "'" * (index + 1)
    for expr in names:
        expr.name = new_name

