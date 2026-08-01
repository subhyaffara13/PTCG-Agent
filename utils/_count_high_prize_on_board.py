
def _count_high_prize_on_board(gs: dict) -> int:
    """Count how many high-prize (prize_yield>=2) Pokemon are on our board."""
    count = 0
    active = gs.get("my_active_pokemon", {})
    if isinstance(active, dict):
        if _get_prize_yield(str(active.get("card_name", ""))) >= 2:
            count += 1
    for bp in gs.get("my_bench", []):
        if isinstance(bp, dict):
            if _get_prize_yield(str(bp.get("card_name", ""))) >= 2:
                count += 1
    return count


def _count_high_prize_on_board(gs: dict) -> int:
    """Count how many high-prize (prize_yield>=2) Pokemon are on our board."""
    count = 0
    active = gs.get("my_active_pokemon", {})
    if isinstance(active, dict):
        if _get_prize_yield(str(active.get("card_name", ""))) >= 2:
            count += 1
    for bp in gs.get("my_bench", []):
        if isinstance(bp, dict):
            if _get_prize_yield(str(bp.get("card_name", ""))) >= 2:
                count += 1
    return count

