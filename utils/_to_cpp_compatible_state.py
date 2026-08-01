
def _to_cpp_compatible_state(gs: dict) -> dict:
    cpp_gs = gs.copy()
    
    def to_str_list(lst):
        if not isinstance(lst, list):
            return []
        return [str(x) for x in lst if x is not None]
        
    def convert_pokemon(poke):
        if not isinstance(poke, dict):
            return poke
        p = poke.copy()
        if "id" in p and p["id"] is not None:
            p["id"] = str(p["id"])
        if "attached" in p:
            p["attached"] = to_str_list(p["attached"])
        return p

    for key in ["my_hand", "my_discard", "my_deck", "opponent_discard", "opponent_deck"]:
        if key in cpp_gs:
            cpp_gs[key] = to_str_list(cpp_gs[key])
            
    for key in ["my_active_pokemon", "opponent_active", "opponent_active_pokemon"]:
        if key in cpp_gs and cpp_gs[key] is not None:
            cpp_gs[key] = convert_pokemon(cpp_gs[key])
            
    for key in ["my_bench", "opponent_bench"]:
        if key in cpp_gs and isinstance(cpp_gs[key], list):
            cpp_gs[key] = [convert_pokemon(p) for p in cpp_gs[key]]
            
    return cpp_gs


def _to_cpp_compatible_state(gs: dict) -> dict:
    cpp_gs = gs.copy()
    
    def to_str_list(lst):
        if not isinstance(lst, list):
            return []
        return [str(x) for x in lst if x is not None]
        
    def convert_pokemon(poke):
        if not isinstance(poke, dict):
            return poke
        p = poke.copy()
        if "id" in p and p["id"] is not None:
            p["id"] = str(p["id"])
        if "attached" in p:
            p["attached"] = to_str_list(p["attached"])
        return p

    for key in ["my_hand", "my_discard", "my_deck", "opponent_discard", "opponent_deck"]:
        if key in cpp_gs:
            cpp_gs[key] = to_str_list(cpp_gs[key])
            
    for key in ["my_active_pokemon", "opponent_active", "opponent_active_pokemon"]:
        if key in cpp_gs and cpp_gs[key] is not None:
            cpp_gs[key] = convert_pokemon(cpp_gs[key])
            
    for key in ["my_bench", "opponent_bench"]:
        if key in cpp_gs and isinstance(cpp_gs[key], list):
            cpp_gs[key] = [convert_pokemon(p) for p in cpp_gs[key]]
            
    return cpp_gs


def _to_cpp_compatible_state(gs: dict) -> dict:
    cpp_gs = gs.copy()
    
    def to_str_list(lst):
        if not isinstance(lst, list):
            return []
        return [str(x) for x in lst if x is not None]
        
    def convert_pokemon(poke):
        if not isinstance(poke, dict):
            return poke
        p = poke.copy()
        if "id" in p and p["id"] is not None:
            p["id"] = str(p["id"])
        if "attached" in p:
            p["attached"] = to_str_list(p["attached"])
        return p

    for key in ["my_hand", "my_discard", "my_deck", "opponent_discard", "opponent_deck"]:
        if key in cpp_gs:
            cpp_gs[key] = to_str_list(cpp_gs[key])
            
    for key in ["my_active_pokemon", "opponent_active", "opponent_active_pokemon"]:
        if key in cpp_gs and cpp_gs[key] is not None:
            cpp_gs[key] = convert_pokemon(cpp_gs[key])
            
    for key in ["my_bench", "opponent_bench"]:
        if key in cpp_gs and isinstance(cpp_gs[key], list):
            cpp_gs[key] = [convert_pokemon(p) for p in cpp_gs[key]]
            
    return cpp_gs

