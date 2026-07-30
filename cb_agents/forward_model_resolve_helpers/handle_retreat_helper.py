from . import Any, logger
from ._apply_status_to_opponent__status_blocks_retreat import _status_blocks_retreat

def handle_retreat_helper(gs: dict, target: str, CardRegistry: Any) -> None:
    # Check if status blocks retreat
    if _status_blocks_retreat(gs.get("my_active_status", "")):
        return
    bench = list(gs.get("my_bench", []))
    if bench:
        old_active = gs.get("my_active_pokemon", {})
        target_idx = None
        if target:
            try:
                target_idx = int(target)
            except ValueError:
                for i, p in enumerate(bench):
                    if isinstance(p, dict) and str(p.get("id")) == target:
                        target_idx = i
                        break
        if target_idx is None or target_idx < 0 or target_idx >= len(bench):
            target_idx = 0
        new_active = bench.pop(target_idx)
        
        retreat_cost = 1
        try:
            card = CardRegistry().get_full_skill(old_active.get("id"))
            if card is not None:
                retreat_cost = card.retreat_cost
        except Exception as e:
            logger.error(f"Failed to retrieve card retreat cost: {e}")
            
        attached = list(old_active.get("attached", []))
        # Per game rules: retreat requires enough energy to pay retreat cost
        if len(attached) < retreat_cost:
            bench.insert(target_idx, new_active)
            return
        removed_energies = []
        for _ in range(retreat_cost):
            removed_energies.append(attached.pop(0))
        old_active["attached"] = attached
        gs["my_discard"] = gs.get("my_discard", []) + removed_energies
        
        bench.append(old_active)
        gs["my_bench"] = bench
        gs["my_active_pokemon"] = new_active

