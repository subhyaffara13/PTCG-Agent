from typing import Any

def _step_hand(gs: dict[str, Any], analyst: Any, router: Any) -> dict[str, Any]:
    from router.bus import HandAnalystPacket
    return router.dispatch("HandAnalyst", HandAnalystPacket(
        hand=gs.get("my_hand", []),
        deck_remaining=gs.get("my_deck_count", 60),
    ))
