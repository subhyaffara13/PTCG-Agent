
def run_iteration(iteration_id: int, forced_archetype: str | None = None, forced_escalation: dict | None = None):
    """Public entry point used by run_guided_iterations.py.

    Wraps run_team_pipeline, accepting optional forced_archetype and
    forced_escalation parameters for the guided-iteration scheduler.
    Returns the iteration result dict from the game runner.
    """
    return run_team_pipeline(iteration_id, forced_archetype=forced_archetype, forced_escalation=forced_escalation)

