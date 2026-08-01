
def transform_match_stmt(builder: IRBuilder, m: MatchStmt) -> None:
    m.accept(MatchVisitor(builder, m))

