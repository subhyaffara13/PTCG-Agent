import logging
import random
logger = logging.getLogger(__name__)
from typing import Any
STATUS_APPLY_ATTACKS = {"poison", "burn", "sleep", "paralyze", "confuse", "toxic"}

from ._resolve_status_effects import _resolve_status_effects
from ._status_helpers import _apply_status_to_opponent
from ._status_helpers import _status_blocks_retreat
from .handle_retreat_helper import handle_retreat_helper
from .handle_attack_helper import handle_attack_helper
from .handle_play_trainer_helper import handle_play_trainer_helper
