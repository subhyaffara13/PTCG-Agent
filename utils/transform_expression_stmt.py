
def transform_expression_stmt(builder: IRBuilder, stmt: ExpressionStmt) -> None:
    if isinstance(stmt.expr, StrExpr):
        # Docstring. Ignore
        return
    # ExpressionStmts do not need to be coerced like other Expressions, so
    # we shouldn't call builder.accept here.
    builder.expression_depth += 1
    builder.reassigned_in_expr = find_walrus_targets(stmt.expr)
    builder.expr_has_suspend = expr_has_suspend(stmt.expr)
    stmt.expr.accept(builder.visitor)
    builder.expression_depth -= 1
    builder.reassigned_in_expr = set()
    builder.expr_has_suspend = False
    builder.flush_keep_alives(stmt.line, scope=KEEP_ALIVE_SHORT_LIVED)
    builder.flush_keep_alives(stmt.line, scope=KEEP_ALIVE_WHOLE_EXPRESSION)

