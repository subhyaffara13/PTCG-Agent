
def _get_nested(d: Union[Dict[str, Any], str], path: Sequence[str]) -> Any:
    cur: Any = d
    if isinstance(cur, str):
        # This shouldn't happen if service keys are pre-parsed correctly
        try:
            cur = json.loads(cur)
        except json.JSONDecodeError:
            verbose_logger.warning(
                "SAP service key or VCAP service is a string but not valid JSON."
            )
            return None
    for k in path:
        if not isinstance(cur, dict):
            verbose_logger.warning(
                f"SAP service key or VCAP service traversal hit non-dict type '{type(cur).__name__}' at key '{k}'."
            )
            return None
        if k not in cur:
            return None
        cur = cur[k]
    return cur

