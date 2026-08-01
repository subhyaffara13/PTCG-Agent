
def handle_time_manager_helper(orchestrator, time_elapsed, legal_actions_list, game_state):
    from router.bus import TimePacket
    from cb_agents.heuristic_pipeline import pipeline

    def _get_f(obj, k, default=None):
        if isinstance(obj, dict): return obj.get(k, default)
        return getattr(obj, k, default)

    time_result = orchestrator.bus.dispatch('TimeManager', TimePacket(
        time_elapsed=time_elapsed, time_limit=600.0, legal_actions=legal_actions_list).__dict__)

    t_dir = _get_f(time_result, 'directive')
    t_act = _get_f(time_result, 'action_override')

    if t_dir == 'FORCE_PASS':
        if 'pass' in legal_actions_list:
            return 'pass'
        elif legal_actions_list:
            return legal_actions_list[0]
        else:
            return 'pass'
    if t_act is not None: return t_act
    if t_dir == 'FAST_MOVE':
        gs_dict = game_state.__dict__ if not isinstance(game_state, dict) else game_state
        best_action, best_score = 'pass', -float('inf')
        for a in legal_actions_list:
            s = pipeline.score_action(a, gs_dict)
            if s > best_score:
                best_score, best_action = s, a
        return best_action
    return None


def handle_time_manager_helper(orchestrator, time_elapsed, legal_actions_list, game_state):
    from router.bus import TimePacket
    from cb_agents.heuristic_pipeline import pipeline

    def _get_f(obj, k, default=None):
        if isinstance(obj, dict): return obj.get(k, default)
        return getattr(obj, k, default)

    time_result = orchestrator.bus.dispatch('TimeManager', TimePacket(
        time_elapsed=time_elapsed, time_limit=600.0, legal_actions=legal_actions_list).__dict__)

    t_dir = _get_f(time_result, 'directive')
    t_act = _get_f(time_result, 'action_override')

    if t_dir == 'FORCE_PASS':
        if 'pass' in legal_actions_list:
            return 'pass'
        elif legal_actions_list:
            return legal_actions_list[0]
        else:
            return 'pass'
    if t_act is not None: return t_act
    if t_dir == 'FAST_MOVE':
        gs_dict = game_state.__dict__ if not isinstance(game_state, dict) else game_state
        best_action, best_score = 'pass', -float('inf')
        for a in legal_actions_list:
            s = pipeline.score_action(a, gs_dict)
            if s > best_score:
                best_score, best_action = s, a
        return best_action
    return None

def handle_time_manager_helper(orchestrator, time_elapsed, legal_actions_list, game_state):
    from router.bus import TimePacket
    from cb_agents.heuristic_pipeline import pipeline

    def _get_f(obj, k, default=None):
        if isinstance(obj, dict): return obj.get(k, default)
        return getattr(obj, k, default)

    time_result = orchestrator.bus.dispatch('TimeManager', TimePacket(
        time_elapsed=time_elapsed, time_limit=600.0, legal_actions=legal_actions_list).__dict__)

    t_dir = _get_f(time_result, 'directive')
    t_act = _get_f(time_result, 'action_override')

    if t_dir == 'FORCE_PASS':
        if 'pass' in legal_actions_list:
            return 'pass'
        elif legal_actions_list:
            return legal_actions_list[0]
        else:
            return 'pass'
    if t_act is not None: return t_act
    if t_dir == 'FAST_MOVE':
        gs_dict = game_state.__dict__ if not isinstance(game_state, dict) else game_state
        best_action, best_score = 'pass', -float('inf')
        for a in legal_actions_list:
            s = pipeline.score_action(a, gs_dict)
            if s > best_score:
                best_score, best_action = s, a
        return best_action
    return None

