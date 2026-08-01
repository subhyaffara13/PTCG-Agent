
def _gs_cache_key(gs: dict) -> tuple:
    return (
        gs.get("turn_number"), gs.get("my_prizes"), gs.get("opponent_prizes"),
        gs.get("my_active_hp"), gs.get("opponent_active_hp"),
        gs.get("my_deck_count"), gs.get("opponent_deck_count"),
        tuple(sorted(gs.get("my_hand", []))),
        tuple(str(x) for x in gs.get("my_bench", [])),
        gs.get("stadium_card"),
    )


def _gs_cache_key(gs: dict) -> tuple:
    return (
        gs.get("turn_number"), gs.get("my_prizes"), gs.get("opponent_prizes"),
        gs.get("my_active_hp"), gs.get("opponent_active_hp"),
        gs.get("my_deck_count"), gs.get("opponent_deck_count"),
        tuple(sorted(gs.get("my_hand", []))),
        tuple(str(x) for x in gs.get("my_bench", [])),
        gs.get("stadium_card"),
    )

