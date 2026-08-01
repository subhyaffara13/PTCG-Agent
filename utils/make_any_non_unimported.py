
def make_any_non_unimported(t: Type) -> Type:
    """Replace all Any types that come from unimported types with special form Any."""
    return t.accept(MakeAnyNonUnimported())

