
def get_archetype_for_iteration(i: int) -> str:
    if i % 100 == 0: return ["aggro", "control", "combo", "utility"][(i // 100) % 4]
    if i % 5 == 0: return ["aggro", "control", "tempo"][(i // 5) % 3]
    return "aggro"


def get_archetype_for_iteration(i: int) -> str:
    if i % 100 == 0: return ["aggro", "control", "combo", "utility"][(i // 100) % 4]
    if i % 5 == 0: return ["aggro", "control", "tempo"][(i // 5) % 3]
    return "aggro"

