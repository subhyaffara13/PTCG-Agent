from ._get_player_idx__count_deck_types import _count_deck_types

def _process_replay_steps(steps, player_idx, card_counter, setup_durations, bench_densities, p_counts, t_counts, e_counts):
    if len(steps) > 1 and len(steps[1]) > player_idx:
        deck = steps[1][player_idx].get("action", [])
        if len(deck) == 60:
            card_counter.update(deck)
            p_c, t_c, e_c = _count_deck_types(deck)
            p_counts.append(p_c); t_counts.append(t_c); e_counts.append(e_c)
            
    setup_dur, bench_sizes = len(steps), []
    for turn_idx, step in enumerate(steps):
        if len(step) > player_idx:
            obs = (step[player_idx].get("observation") or {}).get("current") or {}
            if obs and "players" in obs:
                bench_sizes.append(len(obs["players"][player_idx].get("bench", [])))
            act = step[player_idx].get("action", [])
            obs_dict = step[player_idx].get("observation", {}) or {}
            select = obs_dict.get("select") or {}
            options = select.get("options") or select.get("option") or []
            is_attack = False
            if act and isinstance(act, list) and len(act) > 0:
                opt_idx = act[0]
                if isinstance(opt_idx, int) and 0 <= opt_idx < len(options):
                    chosen_opt = options[opt_idx]
                    if chosen_opt and isinstance(chosen_opt, dict) and chosen_opt.get("type") == 13:
                        is_attack = True
            if is_attack and setup_dur == len(steps):
                setup_dur = turn_idx
    setup_durations.append(setup_dur)
    if bench_sizes: bench_densities.append(sum(bench_sizes) / len(bench_sizes))

