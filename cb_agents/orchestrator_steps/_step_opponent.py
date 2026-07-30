from . import Any, OpponentModel, OpponentModelPacket, RouterBus

def _step_opponent(gs: dict[str, Any], opponent: OpponentModel, router: RouterBus) -> dict[str, Any]:
    active_pokemon = gs.get("opponent_active")
    revealed_active = ""
    if active_pokemon is not None:
        if isinstance(active_pokemon, dict):
            val = active_pokemon.get("id")
            if val is not None:
                revealed_active = str(val)
        else:
            revealed_active = str(active_pokemon)

    opp_pkt = OpponentModelPacket(
        turn                      = int(gs.get("turn_number", 1)),
        newly_played_cards        = gs.get("opponent_revealed", []),
        revealed_active_pokemon   = revealed_active,
        revealed_bench_count      = int(gs.get("opponent_bench_count", 0)),
        revealed_hand_size        = int(gs.get("opponent_hand_size", 0)),
        revealed_prizes_remaining = int(gs.get("opponent_prizes", 6)),
        revealed_discard          = gs.get("opponent_discard", []),
        game_phase                = gs.get("game_phase", "mid"),
    )
    return router.dispatch("OpponentModel", opp_pkt)

