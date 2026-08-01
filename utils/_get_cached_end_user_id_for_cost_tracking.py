
def _get_cached_end_user_id_for_cost_tracking():
    """
    Get cached get_end_user_id_for_cost_tracking function.
    Lazy imports on first call to avoid loading utils.py at import time (60MB saved).
    Subsequent calls use cached function for better performance.
    """
    global _get_end_user_id_for_cost_tracking
    if _get_end_user_id_for_cost_tracking is None:
        from litellm.utils import get_end_user_id_for_cost_tracking

        _get_end_user_id_for_cost_tracking = get_end_user_id_for_cost_tracking
    return _get_end_user_id_for_cost_tracking

