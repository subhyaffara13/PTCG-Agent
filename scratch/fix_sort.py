import re

with open('cb_agents/turn_planner_sort.py', 'r', encoding='utf-8') as f:
    text = f.read()

start_idx = text.find('        def get_priority_rank')
end_idx = text.find('        return sorted(candidates, key=get_priority_rank)')

if start_idx != -1 and end_idx != -1:
    new_func = """        def get_priority_rank(action: str) -> tuple:
            cat_rank = len(order)
            for rank, prefix in enumerate(order):
                if action.startswith(prefix):
                    cat_rank = rank
                    break
            micro_rank = 0
            
            # Combo tag priority logic
            card_id = None
            if ":" in action:
                parts = action.split(":", 2)
                card_id = parts[1]
                if card_id.isdigit():
                    try:
                        c = _registry.get(int(card_id))
                        if c and c.combo_tags:
                            if profile == "setup" and any(t in ("search", "bench", "setup") for t in c.combo_tags):
                                micro_rank -= 4
                            elif profile in ("aggro_push", "closing") and any(t in ("damage", "discard", "boss") for t in c.combo_tags):
                                micro_rank -= 4
                    except Exception:
                        pass
                        
            if action.startswith("play_trainer:"):
                name = action.split(":", 1)[1]
                has_dead = _dead_weight_heuristic(candidates, game_state)
                _discard_search = {"ultra ball", "earthen vessel"}
                if has_dead and any(ds in name.lower() for ds in _discard_search):
                    micro_rank -= 6
                elif "Research" in name or "Professor" in name or "Iono" in name:
                    micro_rank -= 5
                elif "Ball" in name:
                    micro_rank -= 1
            elif action.startswith("bench:"):
                bench_need = 0
                if profile == "setup":
                    bench_need = 5
                elif profile in ("aggro_push", "closing"):
                    bench_need = 2
                if bench_size >= bench_need:
                    micro_rank = 5
                elif my_hand_size < 3 and bench_size == 0:
                    micro_rank = -3
            elif action.startswith("attach_energy:"):
                parts = action.split(":", 2)
                energy_card = parts[1] if len(parts) > 1 else ""
                target_id = parts[2] if len(parts) > 2 else ""
                
                try:
                    from cb_agents.preference_maps import get_energy_preference
                except ImportError:
                    from cb_agents.preference_maps import get_energy_preference
                    
                preferred_energy = get_energy_preference(target_id)
                if target_id and preferred_energy:
                    if preferred_energy != energy_card:
                        micro_rank = 25  # High penalty for wrong color
                        return cat_rank * 5 + micro_rank
                
                if target_id == active.get("id", ""):
                    if active_attached == 0:
                        micro_rank -= 2
                    else:
                        micro_rank -= 1
                else:
                    micro_rank += 2
                    
            elif action.startswith("attack:"):
                micro_rank -= 10
                
            elif action == "pass":
                micro_rank += 20
                
            # Blend Neural Prior
            prior = neural_priors.get(action, 0.0)
            # Subtracting from rank increases priority. A strong prior (e.g. 0.8) subtracts up to 16 from rank.
            neural_bonus = prior * 20.0
            
            return cat_rank * 5 + micro_rank - neural_bonus

"""
    with open('cb_agents/turn_planner_sort.py', 'w', encoding='utf-8') as f:
        f.write(text[:start_idx] + new_func + text[end_idx:])
    print('Replaced get_priority_rank successfully.')
else:
    print('Indices not found.')
