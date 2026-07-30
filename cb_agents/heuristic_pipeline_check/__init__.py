"""
Sub-module: check_lethal, mask_illegal, _calc_sig
"""
import logging
from typing import Dict, List
from cb_agents.card_registry import CardRegistry
logger = logging.getLogger(__name__)
_registry = CardRegistry()
from cb_agents.card_utils import _get_prize_yield

from .check_lethal import check_lethal
from .mask_illegal__calc_sig import mask_illegal
from .mask_illegal__calc_sig import _calc_sig
