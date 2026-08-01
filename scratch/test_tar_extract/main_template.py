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


from utils.compile_extension_on_kaggle import compile_extension_on_kaggle

from utils._update_mcts_module import _update_mcts_module

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
if not isinstance(_existing_deck, list) or len(_existing_deck) != 60:
    DEFAULT_DECK = [
        3, 3, 3, 3, 3, 3, 3, 5, 6, 6,
        11, 19, 19, 65, 66, 304, 305, 676, 676, 676,
        676, 677, 678, 722, 723, 741, 742, 743, 878, 879,
        1079, 1081, 1086, 1086, 1086, 1086, 1102, 1115, 1121, 1122,
        1141, 1142, 1145, 1152, 1152, 1152, 1152, 1171, 1182, 1182,
        1182, 1192, 1219, 1225, 1227, 1227, 1227, 1227, 1231, 1255
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

from utils.make_smart_choice import make_smart_choice

from utils.agent import agent


