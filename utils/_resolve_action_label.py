
def _resolve_action_label(orchestrator, game_state, action_label, select, observation, fallback_action, skills_dir):
    import time
    step_start = time.time()
    action_label = orchestrator.run_turn(game_state)
    if time.time() - step_start > 1.2:
        from .make_smart_choice import make_smart_choice
        return make_smart_choice(select, observation, fallback_action, str(skills_dir)), True
    if hasattr(action_label, 'primary_action'): action_label = action_label.primary_action
    return action_label, False

