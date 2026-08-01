
def test_action_mask(action_mask, env_name=None):
    if not isinstance(action_mask, np.ndarray):
        warnings.warn("Action mask is not a NumPy array")
        return
    if np.isinf(action_mask).any():
        warnings.warn(
            "Action mask contains infinity (np.inf) or negative infinity (-np.inf)"
        )
    if np.isnan(action_mask).any():
        warnings.warn("Action mask contains NaNs")
    if len(action_mask.shape) > 1:
        warnings.warn("Action mask has more than 1 dimension")
    if action_mask.shape == (0,):
        assert False, "Action mask can not be an empty array"
    if action_mask.shape == (1,):
        warnings.warn("Action mask is a single number")
    if not np.can_cast(action_mask.dtype, np.dtype("float64")):
        warnings.warn("Action mask numpy array is not a numeric dtype")
    if (
        np.array_equal(action_mask, np.zeros(action_mask.shape))
        and env_name not in env_all_zeros_obs
    ):
        warnings.warn("Action mask numpy array is all zeros (no legal actions).")
    if not np.array_equal(action_mask, action_mask.astype(bool)):
        warnings.warn(
            "Action mask is not boolean (contains values other than 0 and 1)."
        )

