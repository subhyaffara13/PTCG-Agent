
def no_tie_weights():
    """
    Disable weight tying during loading with `from_pretrained`. This is needed as we want to have access to ALL
    weights in the state_dict during `from_pretrained`, and otherwise tying them would remove them from it, as it's
    called in `post_init` when instantiating.
    """
    from .modeling_utils import PreTrainedModel

    def empty_func(*args, **kwargs):
        pass

    try:
        original_tie_weights = PreTrainedModel.tie_weights
        PreTrainedModel.tie_weights = empty_func

        yield
    finally:
        # Set back the original
        PreTrainedModel.tie_weights = original_tie_weights

