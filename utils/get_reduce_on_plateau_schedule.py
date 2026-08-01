
def get_reduce_on_plateau_schedule(optimizer: Optimizer, **kwargs):
    """
    Create a schedule with a constant learning rate that decreases when a metric has stopped improving.

    Args:
        optimizer ([`~torch.optim.Optimizer`]):
            The optimizer for which to schedule the learning rate.
        kwargs (`dict`, *optional*):
            Extra parameters to be passed to the scheduler. See `torch.optim.lr_scheduler.ReduceLROnPlateau`
            for possible parameters.

    Return:
        `torch.optim.lr_scheduler.ReduceLROnPlateau` with the appropriate schedule.
    """

    return ReduceLROnPlateau(optimizer, **kwargs)

