from . import Any

def _get_attack_damage(gs, CardRegistry):
    try: actual_damage = int(gs.get("my_active_damage", 0))
    except (ValueError, TypeError): actual_damage = 0
    my_active = gs.get("my_active_pokemon", {})
    my_active_id = my_active.get("id") if isinstance(my_active, dict) else my_active
    my_active_name = None
    if not actual_damage and my_active_id is not None and CardRegistry is not None:
        try:
            registry = CardRegistry()
            attached_count = len(my_active.get("attached", [])) if isinstance(my_active, dict) else 0
            actual_damage, my_active_name = registry.get_best_attack_damage_with_name(my_active_id, attached_count)
        except Exception: pass
    if not actual_damage:
        try:
            if CardRegistry is not None and my_active_id is not None:
                card = CardRegistry().get_full_skill(my_active_id)
                if card is not None:
                    actual_damage = int(card.damage_output)
                    my_active_name = card.card_name
        except Exception: pass
    return actual_damage, my_active_name
