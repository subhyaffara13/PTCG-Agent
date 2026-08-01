
def determine_context(change_type: str, archetype: str) -> str:
    if change_type == "deck_swap": return "deck_test"
    if change_type == "strategy_patch":
        return "aggro_test" if archetype in ("aggro", "control", "combo", "utility") else "meta_test"
    return "micro_patch" if change_type == "micro_patch" else "aggro_test"

