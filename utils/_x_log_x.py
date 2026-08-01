
def _x_log_x(tensor):
    """
    Utility function for calculating x log x
    """
    return torch.special.xlogy(tensor, tensor)  # produces correct result for x=0

