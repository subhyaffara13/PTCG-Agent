
def get_greedy_schedule(optimizer: Optimizer, **kwargs):
    """
    Create an adaptive learning rate scheduler that adjusts LR based on training metrics.

    Args:
        optimizer ([`~torch.optim.Optimizer`]):
            The optimizer for which to schedule the learning rate.
        kwargs (`dict`, *optional*):
            Extra parameters passed to the scheduler. See [`GreedyLR`] for possible parameters.

    Return:
        [`GreedyLR`] with the appropriate schedule.
    """
    return GreedyLR(optimizer, **kwargs)

