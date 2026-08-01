
def _map_action(orchestrator, action_label, options, game_state, select):
    from . import get_mapped_indices
    is_energy = (select.get("type") == 7)
    if is_energy and hasattr(orchestrator, "last_energy_target") and orchestrator.last_energy_target:
        return get_mapped_indices(f"target:{orchestrator.last_energy_target}", options, game_state)
    return get_mapped_indices(action_label, options, game_state)

