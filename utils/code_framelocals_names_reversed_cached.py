
def code_framelocals_names_reversed_cached(code: types.CodeType) -> list[str]:
    return list(reversed(code_framelocals_names(code)))

