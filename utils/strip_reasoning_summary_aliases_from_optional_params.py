
def strip_reasoning_summary_aliases_from_optional_params(
    optional_params: dict,
) -> Tuple[dict, Optional[Any]]:
    """Copy optional_params; remove reasoningSummary aliases from top-level and extra_body."""
    op = dict(optional_params)
    rs_val = op.pop("reasoningSummary", None)
    snake_rs_val = op.pop("reasoning_summary", None)
    if rs_val is None:
        rs_val = snake_rs_val
    eb = op.get("extra_body")
    if isinstance(eb, dict):
        eb = dict(eb)
        eb_rs_val = eb.pop("reasoningSummary", None)
        eb_snake_rs_val = eb.pop("reasoning_summary", None)
        if rs_val is None:
            rs_val = eb_rs_val
            if rs_val is None:
                rs_val = eb_snake_rs_val
        if eb:
            op["extra_body"] = eb
        else:
            op.pop("extra_body", None)
    return op, rs_val

