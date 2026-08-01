
def consider_sys_platform(expr: Expression, platform: str) -> int:
    """Consider whether expr is a comparison involving sys.platform.

    Return ALWAYS_TRUE, ALWAYS_FALSE, or TRUTH_VALUE_UNKNOWN.
    """
    # Cases supported:
    # - sys.platform == 'linux'
    # - sys.platform != 'win32'
    # - sys.platform.startswith('win')
    if isinstance(expr, ComparisonExpr):
        # Let's not yet support chained comparisons.
        if len(expr.operators) > 1:
            return TRUTH_VALUE_UNKNOWN
        op = expr.operators[0]
        if op not in ("==", "!="):
            return TRUTH_VALUE_UNKNOWN
        if not is_sys_attr(expr.operands[0], "platform"):
            return TRUTH_VALUE_UNKNOWN
        right = expr.operands[1]
        if not isinstance(right, StrExpr):
            return TRUTH_VALUE_UNKNOWN
        return fixed_comparison(platform, op, right.value)
    elif isinstance(expr, CallExpr):
        if not isinstance(expr.callee, MemberExpr):
            return TRUTH_VALUE_UNKNOWN
        if len(expr.args) != 1 or not isinstance(expr.args[0], StrExpr):
            return TRUTH_VALUE_UNKNOWN
        if not is_sys_attr(expr.callee.expr, "platform"):
            return TRUTH_VALUE_UNKNOWN
        if expr.callee.name != "startswith":
            return TRUTH_VALUE_UNKNOWN
        if platform.startswith(expr.args[0].value):
            return ALWAYS_TRUE
        else:
            return ALWAYS_FALSE
    else:
        return TRUTH_VALUE_UNKNOWN

