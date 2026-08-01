
def _pipeline_action_for_outcome(step: PipelineStep, outcome: str) -> str:
    """
    Map pipeline step outcome to the configured action.

    - pass -> on_pass
    - fail -> on_fail (content/policy intervention)
    - error -> on_error if set, else on_fail (backward compatible)
    """
    if outcome == "pass":
        return step.on_pass
    if outcome == "fail":
        return step.on_fail
    if step.on_error is not None:
        return step.on_error
    return step.on_fail

