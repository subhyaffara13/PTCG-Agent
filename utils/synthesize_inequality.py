
def synthesize_inequality(cls, name: str, op: str, allow_eq: bool) -> ParsedDef:
    return synthesize_comparison(
        cls,
        name,
        allow_eq,
        raise_on_none=True,
        inner=[
            f"if val1 {op} val2: return True",
            f"elif val2 {op} val1: return False",
        ],
    )

