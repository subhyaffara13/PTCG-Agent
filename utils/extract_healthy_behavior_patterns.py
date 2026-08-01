
def extract_healthy_behavior_patterns(iteration_result: Dict[str, Any], behavioral_vectors: Dict[str, Any], learned_dos: dict, save_dos_fn):
    """Extract behavior dos from successful iterations."""
    for label, game in iteration_result.get("games", {}).items():
        if game.get("winner") == "player_b":
            prizes_taken_b = game.get("prizes_taken_b", 0)
            turns = game.get("turns_taken", 999)
            
            if prizes_taken_b >= 4 and turns < 16:
                logger.info("Extracting healthy pattern from overwhelming victory.")
                bv_b = behavioral_vectors.get("player_b")
                if bv_b and bv_b.energy_accel_rate > 0.5:
                    rule = {"condition": "high_accel_wins", "description": "Energy accel > 0.5 strongly correlates with fast wins."}
                    modified = False
                    if "behavior_dos" not in learned_dos:
                        learned_dos["behavior_dos"] = []
                    if rule not in learned_dos["behavior_dos"]:
                        learned_dos["behavior_dos"].append(rule)
                        modified = True
                    if "setup_profiles" not in learned_dos:
                        learned_dos["setup_profiles"] = []
                    if rule not in learned_dos["setup_profiles"]:
                        learned_dos["setup_profiles"].append(rule)
                        modified = True
                    if modified:
                        save_dos_fn()

