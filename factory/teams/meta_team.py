import logging
import json
from pathlib import Path
from collections import Counter

logger = logging.getLogger("MetaTeam")

class MetaTeam:
    def __init__(self, dataset_dir: str = "dataset", log_dir: str = "logs", skills_dir: str = "skills"):
        self.dataset_dir = Path(dataset_dir)
        self.kaggle_replays_dir = Path(log_dir) / "kaggle_replays"
        self.skills_dir = Path(skills_dir)

    def analyze_meta(self) -> dict:
        """Analyzes external datasets and downloaded Kaggle JSON replays for meta shifts."""
        logger.info("Meta Team starting dataset analysis...")
        results = {"found_new_archetypes": False, "meta_shifts": {}, "archetype_counts": {}}
        
        # Load deck archetypes signature cards
        arch_data = {}
        arch_file = self.skills_dir / "deck_archetypes.json"
        if arch_file.exists():
            try:
                arch_data = json.loads(arch_file.read_text(encoding="utf-8")).get("archetypes", {})
            except Exception as e:
                logger.error(f"Failed to load deck archetypes for analysis: {e}")

        # Scan both directories
        replays = []
        for d in (self.dataset_dir, self.kaggle_replays_dir):
            if d.exists():
                replays.extend(list(d.glob("*.json")))
                
        if not replays:
            logger.info("Meta Team found no replay JSONs to analyze.")
            return results

        logger.info(f"Meta Team found {len(replays)} replays! Processing...")
        archetype_counter = Counter()
        
        for path in replays:
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                steps = data.get("steps", [])
                # The deck list is normally in step 1's action for each player
                if len(steps) > 1:
                    for player_idx in (0, 1):
                        if player_idx < len(steps[1]):
                            deck = steps[1][player_idx].get("action", [])
                            if isinstance(deck, list) and len(deck) == 60:
                                # Determine archetype by matching signature cards
                                best_arch = "utility"
                                max_matches = 0
                                # Convert deck cards to strings/names for signature comparison
                                deck_strs = [str(c) for c in deck]
                                for arch, config in arch_data.items():
                                    sigs = config.get("signature_cards", [])
                                    # Count matches
                                    matches = sum(1 for c in deck_strs if c in sigs)
                                    if matches > max_matches:
                                        max_matches = matches
                                        best_arch = arch
                                archetype_counter[best_arch] += 1
            except Exception as e:
                logger.debug(f"Failed to parse replay {path.name}: {e}")

        if archetype_counter:
            results["found_new_archetypes"] = True
            results["archetype_counts"] = dict(archetype_counter)
            most_common = archetype_counter.most_common(1)[0][0]
            results["meta_shifts"] = {"trend": f"dominant_{most_common}"}
            logger.info(f"Meta Team analysis complete. Most common archetype: {most_common}")
        
        return results
