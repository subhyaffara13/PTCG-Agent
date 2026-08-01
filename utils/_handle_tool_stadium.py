
def _handle_tool_stadium(gs, base_name, CardRegistry, target):
    if any(k in base_name for k in {"choice belt", "bravery charm", "forest seal", "canceling cologne", "tool"}):
        valid_targets = []
        if isinstance(gs.get("my_active_pokemon"), dict) and gs["my_active_pokemon"]:
            valid_targets.append("active")
        for i, _ in enumerate(gs.get("my_bench", [])):
            valid_targets.append(f"bench_{i}")
        if valid_targets:
            tgt = random.choice(valid_targets)
            if tgt == "active":
                poke = gs["my_active_pokemon"]
            else:
                idx = int(tgt.split("_")[1])
                bench_pokes = list(gs.get("my_bench", []))
                if 0 <= idx < len(bench_pokes):
                    poke = bench_pokes[idx]
                else:
                    poke = gs.get("my_active_pokemon", {})
            if isinstance(poke, dict):
                tools = poke.get("tools", [])
                tools.append(base_name)
                poke["tools"] = tools
                gs["my_active_pokemon"] = poke
        return True
    if any(k in base_name for k in {"stadium", "peak", "temple", "artazon", "watchtower", "mountain"}):
        try:
            if CardRegistry is not None:
                c = CardRegistry().get_full_skill(target)
                if c and getattr(c, 'trainer_subtype', None) and c.trainer_subtype.name == "STADIUM":
                    gs["stadium_card"] = base_name
        except Exception:
            gs["stadium_card"] = base_name
        return True
    return False


def _handle_tool_stadium(gs, base_name, CardRegistry, target):
    if any(k in base_name for k in {"choice belt", "bravery charm", "forest seal", "canceling cologne", "tool"}):
        valid_targets = []
        if isinstance(gs.get("my_active_pokemon"), dict) and gs["my_active_pokemon"]:
            valid_targets.append("active")
        for i, _ in enumerate(gs.get("my_bench", [])):
            valid_targets.append(f"bench_{i}")
        if valid_targets:
            tgt = random.choice(valid_targets)
            if tgt == "active":
                poke = gs["my_active_pokemon"]
            else:
                idx = int(tgt.split("_")[1])
                bench_pokes = list(gs.get("my_bench", []))
                if 0 <= idx < len(bench_pokes):
                    poke = bench_pokes[idx]
                else:
                    poke = gs.get("my_active_pokemon", {})
            if isinstance(poke, dict):
                tools = poke.get("tools", [])
                tools.append(base_name)
                poke["tools"] = tools
                gs["my_active_pokemon"] = poke
        return True
    if any(k in base_name for k in {"stadium", "peak", "temple", "artazon", "watchtower", "mountain"}):
        try:
            if CardRegistry is not None:
                c = CardRegistry().get_full_skill(target)
                if c and getattr(c, 'trainer_subtype', None) and c.trainer_subtype.name == "STADIUM":
                    gs["stadium_card"] = base_name
        except Exception:
            gs["stadium_card"] = base_name
        return True
    return False

