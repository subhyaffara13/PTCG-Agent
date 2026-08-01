
def _update_behavior_dos(extractor, player_name_or_id, setup_durs, bench_dens):
    if not setup_durs:
        return
    behavior_do = {
        "player": player_name_or_id,
        "avg_setup_duration": round(sum(setup_durs)/len(setup_durs), 1),
        "avg_bench_density": round(sum(bench_dens)/len(bench_dens) if bench_dens else 0.0, 1)
    }
    extractor.learned_dos["behavior_dos"] = [
        b for b in extractor.learned_dos.get("behavior_dos", [])
        if b.get("player") != player_name_or_id
    ] + [behavior_do]
    extractor.learned_dos["setup_profiles"] = [
        b for b in extractor.learned_dos.get("setup_profiles", [])
        if b.get("player") != player_name_or_id
    ] + [behavior_do]

