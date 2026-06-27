"""
run_factory_utils.py
--------------------
Core pipeline logic extracted from run_factory.py.
"""

import logging

from run_factory_utils_helpers import run_team_pipeline as _run_team_pipeline
run_team_pipeline = _run_team_pipeline

logger = logging.getLogger("run_factory")

def run_iteration(iteration_id: int, forced_archetype: str = None, forced_escalation: dict = None):
    """Public entry point used by run_guided_iterations.py.

    Wraps run_team_pipeline, accepting optional forced_archetype and
    forced_escalation parameters for the guided-iteration scheduler.
    Returns the iteration result dict from the game runner.
    """
    return run_team_pipeline(iteration_id, forced_archetype=forced_archetype, forced_escalation=forced_escalation)
