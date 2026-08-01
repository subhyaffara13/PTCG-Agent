"""
factory/parallel_runner_pool.py

Provides configuration schemas and the module-level execution worker
for running game iterations in separate processes.
"""

import sys
import os

# Clean up sys.path to prevent kaggle_environments path pollution from breaking imports
sys.path = [p for p in sys.path if "kaggle_environments" not in p]
cwd = os.getcwd()
if cwd not in sys.path:
    sys.path.insert(0, cwd)

import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class GameConfig:
    """
    Configuration for a single game to run.
    """
    iteration_id: int
    version_a: str
    version_b: str
    deck_a: Any = None
    deck_b: Any = None
    reasoning_a: dict = field(default_factory=dict)
    reasoning_b: dict = field(default_factory=dict)
    label: str = ""


@dataclass
class GameResult:
    """
    Aggregated result from a single game run.
    """
    config: GameConfig
    result: Optional[Dict[str, Any]] = None
    success: bool = True
    error: str = ""


from utils._run_single_game import _run_single_game
