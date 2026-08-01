
def infer_reachability_of_if_statement(s: IfStmt, options: Options) -> None:
    for i in range(len(s.expr)):
        result = infer_condition_value(s.expr[i], options)
        if result in (ALWAYS_FALSE, MYPY_FALSE):
            # The condition is considered always false, so we skip the if/elif body.
            mark_block_unreachable(s.body[i])
        elif result in (ALWAYS_TRUE, MYPY_TRUE):
            # This condition is considered always true, so all of the remaining
            # elif/else bodies should not be checked.
            if result == MYPY_TRUE:
                # This condition is false at runtime; this will affect
                # import priorities.
                mark_block_mypy_only(s.body[i])
            for body in s.body[i + 1 :]:
                mark_block_unreachable(body)

            # Make sure else body always exists and is marked as
            # unreachable so the type checker always knows that
            # all control flow paths will flow through the if
            # statement body.
            if not s.else_body:
                s.else_body = Block([])
            mark_block_unreachable(s.else_body)
            break

