
def wrong_type_arg_count(low: int, high: int, act: str, name: str) -> str:
    if low == high:
        s = f"{low} type arguments"
        if low == 0:
            s = "no type arguments"
        elif low == 1:
            s = "1 type argument"
    else:
        s = f"between {low} and {high} type arguments"
    if act == "0":
        act = "none"
    return f'"{name}" expects {s}, but {act} given'

