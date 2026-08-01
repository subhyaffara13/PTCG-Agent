
def _policy_from_bool(b):
    # For backward compatibility
    return CheckpointPolicy.MUST_SAVE if b else CheckpointPolicy.PREFER_RECOMPUTE

