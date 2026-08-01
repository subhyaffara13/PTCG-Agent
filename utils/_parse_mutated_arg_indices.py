
def _parse_mutated_arg_indices(s: str) -> set[int]:
    return {int(x) for x in s.split(",") if x}

