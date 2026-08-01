
def make_any_non_explicit(t: Type) -> Type:
    """Replace all Any types within in with Any that has attribute 'explicit' set to False"""
    return t.accept(MakeAnyNonExplicit())

