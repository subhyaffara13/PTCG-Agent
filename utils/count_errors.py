
def count_errors(msgs: list[str]) -> int:
    return len([x for x in msgs if " error: " in x])

