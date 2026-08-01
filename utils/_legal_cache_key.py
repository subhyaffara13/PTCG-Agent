
def _legal_cache_key(gs: dict) -> tuple:
    return (
        gs.get("turn_number"), gs.get("select_prize"),
        gs.get("supporter_played_this_turn"),
        gs.get("boss_prob", 0.0),
        gs.get("prize_certainty", 0.0),
        frozenset(gs.get("prized_card_ids", {}).items()),
        tuple(sorted(gs.get("my_hand", []))),
        tuple(sorted(
            str(p.get("id")) for p in gs.get("my_bench", []) if isinstance(p, dict)
        )),
    )


def _legal_cache_key(gs: dict) -> tuple:
    return (
        gs.get("turn_number"), gs.get("select_prize"),
        gs.get("supporter_played_this_turn"),
        gs.get("boss_prob", 0.0),
        gs.get("prize_certainty", 0.0),
        frozenset(gs.get("prized_card_ids", {}).items()),
        tuple(sorted(gs.get("my_hand", []))),
        tuple(sorted(
            str(p.get("id")) for p in gs.get("my_bench", []) if isinstance(p, dict)
        )),
    )

