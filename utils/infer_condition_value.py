
def infer_condition_value(expr: Expression, options: Options) -> int:
    """Infer whether the given condition is always true/false.

    Return ALWAYS_TRUE if always true, ALWAYS_FALSE if always false,
    MYPY_TRUE if true under mypy and false at runtime, MYPY_FALSE if
    false under mypy and true at runtime, else TRUTH_VALUE_UNKNOWN.
    """
    if isinstance(expr, UnaryExpr) and expr.op == "not":
        positive = infer_condition_value(expr.expr, options)
        return inverted_truth_mapping[positive]

    pyversion = options.python_version
    name = ""

    result = TRUTH_VALUE_UNKNOWN
    if isinstance(expr, NameExpr):
        name = expr.name
    elif isinstance(expr, MemberExpr):
        name = expr.name
    elif isinstance(expr, OpExpr):
        if expr.op not in ("or", "and"):
            return TRUTH_VALUE_UNKNOWN

        left = infer_condition_value(expr.left, options)
        right = infer_condition_value(expr.right, options)
        results = {left, right}
        if expr.op == "or":
            if ALWAYS_TRUE in results:
                return ALWAYS_TRUE
            elif MYPY_TRUE in results:
                return MYPY_TRUE
            elif left == right == MYPY_FALSE:
                return MYPY_FALSE
            elif results <= {ALWAYS_FALSE, MYPY_FALSE}:
                return ALWAYS_FALSE
        elif expr.op == "and":
            if ALWAYS_FALSE in results:
                return ALWAYS_FALSE
            elif MYPY_FALSE in results:
                return MYPY_FALSE
            elif left == right == ALWAYS_TRUE:
                return ALWAYS_TRUE
            elif results <= {ALWAYS_TRUE, MYPY_TRUE}:
                return MYPY_TRUE
        return TRUTH_VALUE_UNKNOWN
    else:
        result = consider_sys_version_info(expr, pyversion)
        if result == TRUTH_VALUE_UNKNOWN:
            result = consider_sys_platform(expr, options.platform)
    if result == TRUTH_VALUE_UNKNOWN:
        if name == "PY2":
            result = ALWAYS_FALSE
        elif name == "PY3":
            result = ALWAYS_TRUE
        elif name == "MYPY" or name == "TYPE_CHECKING":
            result = MYPY_TRUE
        elif name in options.always_true:
            result = ALWAYS_TRUE
        elif name in options.always_false:
            result = ALWAYS_FALSE
    return result

