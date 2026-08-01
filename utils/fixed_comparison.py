
def fixed_comparison(left: Targ, op: str, right: Targ) -> int:
    rmap = {False: ALWAYS_FALSE, True: ALWAYS_TRUE}
    if op == "==":
        return rmap[left == right]
    if op == "!=":
        return rmap[left != right]
    if op == "<=":
        return rmap[left <= right]
    if op == ">=":
        return rmap[left >= right]
    if op == "<":
        return rmap[left < right]
    if op == ">":
        return rmap[left > right]
    return TRUTH_VALUE_UNKNOWN

