
def make_suggestion_anys(t: TType) -> TType:
    """Make all anys in the type as coming from the suggestion engine.

    This keeps those Anys from influencing constraint generation,
    which allows us to do better when refining types.
    """
    return cast(TType, t.accept(MakeSuggestionAny()))

