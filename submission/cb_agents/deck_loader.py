import csv
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def load_deck_base_list(skills_dir: Path) -> dict:
    """Loads base deck counts from deck_new.csv or deck.csv."""
    for filename in ["cb_agents/deck_new.csv", "deck.csv"]:
        path = Path(filename)
        if not path.exists():
            path = skills_dir.parent / filename
        if path.exists():
            try:
                deck_dict = {}
                with open(path, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        deck_dict[int(row["card_id"])] = int(row["count"])
                return deck_dict
            except Exception as e:
                logger.warning(f"Deck CSV load failed for {path}: {e}")
    return {}

def load_hand_analyst_configs(agent, shared_context):
    """Loads strategic thresholds and tip overrides."""
    agent.strategy_tips = {"priority_modifiers": {}}
    tips_path = agent.skills_dir / "strategy_tips.json"
    if tips_path.exists():
        try:
            agent.strategy_tips = json.loads(tips_path.read_text(encoding="utf-8"))
        except Exception as e:
            logger.error(f"Failed strategy_tips load: {e}")

    agent.strategy_thresholds = {}
    if shared_context:
        agent.strategy_thresholds = shared_context.get_config(str(agent.skills_dir), "strategy_thresholds.json")
    else:
        try:
            from cb_agents.context import SharedContext
            agent.strategy_thresholds = SharedContext().get_config(str(agent.skills_dir), "strategy_thresholds.json")
        except Exception as e:
            logger.debug(f"Failed to load strategy_thresholds from context fallback: {e}")
