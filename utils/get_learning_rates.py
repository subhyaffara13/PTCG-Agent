
def get_learning_rates(self) -> list[float]:
    """
    Returns the learning rate of each parameter from self.optimizer.
    """
    if self.optimizer is None:
        raise ValueError("Trainer optimizer is None, please make sure you have setup the optimizer before.")
    return [group["lr"] for group in self.optimizer.param_groups]

