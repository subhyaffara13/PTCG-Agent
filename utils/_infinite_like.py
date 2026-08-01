
def _infinite_like(tensor):
    """
    Helper function for obtaining infinite KL Divergence throughout
    """
    return torch.full_like(tensor, inf)

