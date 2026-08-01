
def _operator_cost(op_entry: tuple[CallableOperator, str, str]) -> int:
    """Sort key for Cost Based Ordering of specifier operators in _filter_versions.

    Operators run sequentially on a shrinking candidate set, so operators that
    reject the most versions should run first to minimize work for later ones.

    Tier 0: Exact equality (==, ===), likely to narrow candidates to one version
    Tier 1: Range checks (>=, <=, >, <), cheap and usually reject a large portion
    Tier 2: Wildcard equality (==.*) and compatible release (~=), more expensive
    Tier 3: Exact !=, cheap but rarely rejects
    Tier 4: Wildcard !=.*, expensive and rarely rejects
    """
    _, ver, op = op_entry
    if op == "==":
        return 0 if not ver.endswith(".*") else 2
    if op in (">=", "<=", ">", "<"):
        return 1
    if op == "~=":
        return 2
    if op == "!=":
        return 3 if not ver.endswith(".*") else 4
    if op == "===":
        return 0

    raise ValueError(f"Unknown operator: {op!r}")  # pragma: no cover


def _operator_cost(op_entry: tuple[CallableOperator, str, str]) -> int:
    """Sort key for Cost Based Ordering of specifier operators in _filter_versions.

    Operators run sequentially on a shrinking candidate set, so operators that
    reject the most versions should run first to minimize work for later ones.

    Tier 0: Exact equality (==, ===), likely to narrow candidates to one version
    Tier 1: Range checks (>=, <=, >, <), cheap and usually reject a large portion
    Tier 2: Wildcard equality (==.*) and compatible release (~=), more expensive
    Tier 3: Exact !=, cheap but rarely rejects
    Tier 4: Wildcard !=.*, expensive and rarely rejects
    """
    _, ver, op = op_entry
    if op == "==":
        return 0 if not ver.endswith(".*") else 2
    if op in (">=", "<=", ">", "<"):
        return 1
    if op == "~=":
        return 2
    if op == "!=":
        return 3 if not ver.endswith(".*") else 4
    if op == "===":
        return 0

    raise ValueError(f"Unknown operator: {op!r}")  # pragma: no cover

