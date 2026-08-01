
def synthesize_equality(cls, name: str, converse: str) -> ParsedDef:
    return synthesize_comparison(
        cls,
        name,
        allow_eq=True,
        raise_on_none=False,
        inner=[f"if val1 {converse} val2: return False"],
    )

