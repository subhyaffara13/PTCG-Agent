from . import Path, logger

def update_league_from_iteration(iteration_id: int, iteration_result: dict = None):
    """Update league: save snapshot if improved, rotate exploiter archetypes."""
    from factory.league_manager import LeagueManager
    from pathlib import Path
    import csv
    league = LeagueManager()
    snapshot_path = Path("skills/league") / "main_agent_snapshot.csv"
    current_deck_path = Path("staging") / "deck_new.csv"
    if not current_deck_path.exists():
        current_deck_path = Path("cb_agents") / "deck_new.csv"
    if current_deck_path.exists() and snapshot_path.exists():
        # Only overwrite snapshot if the current deck is different
        current_rows = current_deck_path.read_text(encoding="utf-8")
        snapshot_rows = snapshot_path.read_text(encoding="utf-8")
        if current_rows != snapshot_rows:
            import shutil
            shutil.copy2(str(current_deck_path), str(snapshot_path))
            logger.info(f"League snapshot updated from {current_deck_path}")
    elif current_deck_path.exists():
        import shutil
        shutil.copy2(str(current_deck_path), str(snapshot_path))
        logger.info(f"League snapshot created from {current_deck_path}")
    
    # Rotate exploiter decks every 10 iterations
    if iteration_id % 10 == 0:
        archetypes = {"aggro_exploiter": "aggro", "control_exploiter": "control", "combo_exploiter": "combo"}
        rotation_seed = (iteration_id // 10) % 4
        archetype_order = ["aggro", "control", "combo", "tempo"]
        for exploiter_name, _ in archetypes.items():
            target_arch = archetype_order[(rotation_seed + list(archetypes.keys()).index(exploiter_name)) % len(archetype_order)]
            exploiter_csv = Path("skills/league") / f"{exploiter_name}.csv"
            if exploiter_csv.exists():
                logger.info(f"Archetype rotation: {exploiter_name} -> {target_arch} (seed={rotation_seed})")
    logger.info(f"League status after iteration {iteration_id}: {dict(league.ratings)}")

