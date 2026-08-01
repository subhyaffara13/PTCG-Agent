
def infer_reachability_of_match_statement(s: MatchStmt, options: Options) -> None:
    for i, guard in enumerate(s.guards):
        pattern_value = infer_pattern_value(s.patterns[i])

        if guard is not None:
            guard_value = infer_condition_value(guard, options)
        else:
            guard_value = ALWAYS_TRUE

        if pattern_value in (ALWAYS_FALSE, MYPY_FALSE) or guard_value in (
            ALWAYS_FALSE,
            MYPY_FALSE,
        ):
            # The case is considered always false, so we skip the case body.
            mark_block_unreachable(s.bodies[i])
        elif pattern_value in (ALWAYS_TRUE, MYPY_TRUE) and guard_value in (ALWAYS_TRUE, MYPY_TRUE):
            for body in s.bodies[i + 1 :]:
                mark_block_unreachable(body)

        if guard_value == MYPY_TRUE:
            # This condition is false at runtime; this will affect
            # import priorities.
            mark_block_mypy_only(s.bodies[i])

