"""
run_factory_utils.py
--------------------
Core pipeline logic extracted from run_factory.py.
"""

import logging

from run_factory_utils_helpers import run_team_pipeline as _run_team_pipeline
run_team_pipeline = _run_team_pipeline

logger = logging.getLogger("run_factory")

from utils.run_iteration import run_iteration
