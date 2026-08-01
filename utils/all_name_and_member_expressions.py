
def all_name_and_member_expressions(node: Expression) -> tuple[list[NameExpr], list[MemberExpr]]:
    v = NameAndMemberCollector()
    node.accept(v)
    return (v.name_exprs, v.member_exprs)

