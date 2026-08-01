import json
import logging
import os
import sys
import datetime
from pathlib import Path

# Setup basic log capture
logger = logging.getLogger(__name__)

# Add agent directory to sys.path to ensure imports find cb_agents and router
agent_dir = str(Path(__file__).parent.resolve()) if "__file__" in globals() and globals()["__file__"] else os.getcwd()
if agent_dir not in sys.path:
    sys.path.insert(0, agent_dir)

import time
_GLOBAL_START_TIME = time.time()


from utils.compile_extension_on_kaggle import compile_extension_on_kaggle

from utils._update_mcts_module import _update_mcts_module

from utils.load_deck_on_kaggle import load_deck_on_kaggle

# Run compilation on Kaggle immediately at module load time (best-effort)
compile_extension_on_kaggle()

# Try to import Orchestrator from cb_agents if not already present
if globals().get("orchestrator") is None:
    try:
        from cb_agents.orchestrator import Orchestrator
        orchestrator = Orchestrator(
            skills_dir=os.path.join(agent_dir, "skills"),
            log_dir=os.path.join(agent_dir, "logs")
        )
        orchestrator.start_game()
    except Exception as global_err:
        logger.error(f"Global orchestrator initialization failed: {global_err}")
        orchestrator = None

# Default deck from the competition environment if not already defined (single-file mode)
_existing_deck = globals().get("DEFAULT_DECK")
if _existing_deck is None:
    DEFAULT_DECK = [
        957, 957, 957, 957, 979, 979, 979, 979, 210, 210,
        210, 210, 1121, 1121, 1121, 1121, 1102, 1102, 1102, 1102,
        1213, 1213, 1213, 1213, 1206, 1206, 1206, 1206, 1182, 1182,
        1182, 1182, 1123, 1123, 1123, 1123, 1116, 1116, 1118, 1118,
        1081, 1081, 1097, 1097, 1122, 1122, 6, 6, 6, 6,
        6, 6, 6, 6, 4, 4, 4, 4, 4, 4
    ]

    try:
        _deck_csv_path = None
        if "__file__" in globals() and globals()["__file__"]:
            _deck_csv_path = Path(__file__).parent / "deck.csv"
        if not _deck_csv_path or not _deck_csv_path.exists():
            _deck_csv_path = Path("deck.csv")
        if not _deck_csv_path.exists():
            _deck_csv_path = Path("submission/deck.csv")
        
        if _deck_csv_path.exists():
            import csv
            _loaded_deck = []
            with open(_deck_csv_path, "r", encoding="utf-8") as _f:
                _reader = csv.DictReader(_f)
                for _row in _reader:
                    _loaded_deck.extend([int(_row["card_id"])] * int(_row["count"]))
            if len(_loaded_deck) == 60:
                DEFAULT_DECK = _loaded_deck
    except Exception:
        pass



from typing import Any

from utils.get_val import get_val

from utils._log_action_exception import _log_action_exception

_registry = None

from utils.resolve_option_names import resolve_option_names

from utils.get_mapped_indices import get_mapped_indices


from utils.make_smart_choice import make_smart_choice

from utils.agent import agent


