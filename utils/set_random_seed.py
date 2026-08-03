import random

def set_random_seed(seed=123):
    """Set random seed manually to get deterministic results"""
    random.seed(seed)
    numpy.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

