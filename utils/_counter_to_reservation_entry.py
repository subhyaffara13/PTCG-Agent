from typing import Any, Dict

def _counter_to_reservation_entry(
    counter: _BudgetCounter,
    reserved_cost: float,
) -> Dict[str, Any]:
    return {
        "counter_key": counter.counter_key,
        "entity_type": counter.entity_type,
        "entity_id": counter.entity_id,
        "reserved_cost": reserved_cost,
        "applied_adjustment": 0.0,
    }

