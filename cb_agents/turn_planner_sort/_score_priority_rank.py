from cb_agents.turn_planner_sort._sort_constants import _EARLY_BENCH_ORDER
from cb_agents.turn_planner_sort._sort_constants import _PRIORITY_RULES
from cb_agents.turn_planner_heuristics import _registry
from ._score_play_trainer_rank import _score_play_trainer_rank
from ._score_bench_rank import _score_bench_rank
from ._score_attach_energy_rank import _score_attach_energy_rank
from ._spr_boss_bonus import _score_boss_bonus
from ._spr_combo_bonus import _score_combo_bonus

def _get_priority_rank(action, order, game_state, neural_priors):
    cat_rank = len(order)
    for rank, prefix in enumerate(order):
        if action.startswith(prefix):
            cat_rank = rank
            break
    micro_rank = _score_boss_bonus(action, game_state) + _score_combo_bonus(action, game_state)
    active = game_state.get("my_active_pokemon") or {}
    active_attached = len(active.get("attached", []) or active.get("energies", [])) if isinstance(active, dict) else 0
    bench_size = len(game_state.get("my_bench", []))
    my_hand_size = len(game_state.get("my_hand", []))
    profile = game_state.get("priority_profile", "aggro_push")
    if action.startswith("play_trainer:"):
        micro_rank += _score_play_trainer_rank(action, game_state)
    elif action.startswith("bench:"):
        micro_rank += _score_bench_rank(action, game_state, profile, bench_size, my_hand_size)
    elif action.startswith("attach_energy:"):
        micro_rank += _score_attach_energy_rank(action, game_state, active_attached, active)
    elif action.startswith("evolve:"):
        micro_rank -= 8
    elif action.startswith("retreat:"):
        retreat_penalty = 35
        boost = game_state.get("retreat_score_boost", 0.0)
        if boost > 0:
            retreat_penalty = -5
        else:
            hp = game_state.get("my_active_hp", 100)
            if hp <= 40:
                retreat_penalty = 5
            else:
                active_energy_count = len(active.get("attached", []) or active.get("energies", [])) if isinstance(active, dict) else 0
                if active_energy_count == 0:
                    retreat_penalty = 0
        micro_rank += retreat_penalty
    elif action == "pass":
        dc = game_state.get("my_deck_count", 60)
        opp_dc = game_state.get("opponent_deck_count", 60)
        if opp_dc < dc and opp_dc < 8:
            micro_rank -= 12
        else:
            micro_rank += 20
    prior = neural_priors.get(action, 0.0)
    neural_bonus = prior * 20.0
    return cat_rank * 15 + micro_rank - neural_bonus
