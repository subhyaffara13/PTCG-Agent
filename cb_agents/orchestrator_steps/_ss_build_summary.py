def _build_board_summary(gs, orchestrator):
    my_bench = gs.get("my_bench", []); bench_count = len(my_bench) if isinstance(my_bench, list) else 0
    my_active = gs.get("my_active_pokemon")
    energy_attached = gs.get("_cached_energy_attached", 0)
    if energy_attached == 0:
        if isinstance(my_active, dict): energy_attached += len(my_active.get("attached", []))
        if isinstance(my_bench, list):
            for p in my_bench:
                if isinstance(p, dict): energy_attached += len(p.get("attached", []))
    hand_score = gs.get("hand_score", 5.0)
    boss_prob = 0.0; iono_prob = 0.0; path_prob = 0.0; hammer_prob = 0.0
    if hasattr(orchestrator, "belief_tracker") and orchestrator.belief_tracker:
        boss_prob = orchestrator.belief_tracker.probability_opponent_holds("boss's orders")
        iono_prob = orchestrator.belief_tracker.probability_opponent_holds("iono")
        path_prob = orchestrator.belief_tracker.probability_opponent_holds("path to the peak")
        hammer_prob = orchestrator.belief_tracker.probability_opponent_holds("crushing hammer")
    opponent_archetype = "unknown"; archetype_confidence = 0.0
    if hasattr(orchestrator, "opponent_model"):
        om = orchestrator.opponent_model
        opponent_archetype = getattr(om, "identified_archetype", "unknown")
        archetype_confidence = getattr(om, "archetype_confidence", 0.0)
    my_active_hp = my_active.get("hp", 100) if isinstance(my_active, dict) else 100
    return {"prizes": gs.get("my_prizes", 6), "opponent_prizes": gs.get("opponent_prizes", 6),
            "bench_count": bench_count, "hand_score": hand_score, "energy_attached": energy_attached,
            "turn_number": gs.get("turn_number", 1), "boss_prob": boss_prob, "iono_prob": iono_prob,
            "path_prob": path_prob, "hammer_prob": hammer_prob,
            "my_prizes_remaining": gs.get("my_prizes", 6), "opponent_prizes_remaining": gs.get("opponent_prizes", 6),
            "my_bench_count": bench_count, "opponent_archetype": opponent_archetype,
            "opponent_archetype_confidence": archetype_confidence, "my_active_hp": my_active_hp,
            "bench_has_attacker": bench_count > 0, "priority_profile": gs.get("priority_profile", "balanced")}
