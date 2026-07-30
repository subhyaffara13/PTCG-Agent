def _resolve_action_label(orchestrator, game_state, action_label, select, observation, fallback_action, skills_dir):
    import time
    step_start = time.time()
    action_label = orchestrator.run_turn(game_state)
    if time.time() - step_start > 1.2:
        from .make_smart_choice import make_smart_choice
        return make_smart_choice(select, observation, fallback_action, str(skills_dir)), True
    if hasattr(action_label, 'primary_action'): action_label = action_label.primary_action
    return action_label, False

def _map_action(orchestrator, action_label, options, game_state, select):
    from . import get_mapped_indices
    is_energy = (select.get("type") == 7)
    if is_energy and hasattr(orchestrator, "last_energy_target") and orchestrator.last_energy_target:
        return get_mapped_indices(f"target:{orchestrator.last_energy_target}", options, game_state)
    return get_mapped_indices(action_label, options, game_state)
