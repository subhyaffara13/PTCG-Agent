
def _extract_healthy_pattern(iteration_result, behavioral_vectors, learned_dos, save_dos_fn):
    import logging
    logger = logging.getLogger(__name__)
    for label, game in iteration_result.get("games", {}).items():
        if game.get("winner") != "player_b": continue
        prizes_taken_b, turns = game.get("prizes_taken_b", 0), game.get("turns_taken", 999)
        if prizes_taken_b < 4 or turns >= 16: continue
        logger.info("Extracting healthy pattern from overwhelming victory.")
        bv_b = behavioral_vectors.get("player_b")
        if bv_b and bv_b.energy_accel_rate > 0.5:
            rule = {"condition": "high_accel_wins", "description": "Energy accel > 0.5 strongly correlates with fast wins."}
            modified = False
            for key in ("behavior_dos", "setup_profiles"):
                if key not in learned_dos: learned_dos[key] = []
                if rule not in learned_dos[key]:
                    learned_dos[key].append(rule); modified = True
            if modified: save_dos_fn()

