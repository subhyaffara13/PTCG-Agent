
def match_one_event(
    event_a: dict[Any, Any],
    event_b: dict[Any, Any],
    memberships: dict[str, set[Any]],
    pg_name: str,
) -> MatchInfo:
    op_a = Op(event_a, memberships, pg_name)
    op_b = Op(event_b, memberships, pg_name)
    return op_a.match(op_b)

