
def set_deterministic() -> None:
    """Make torch manual seed deterministic."""

    torch.manual_seed(MAIN_RANDOM_SEED)
    random.seed(MAIN_RANDOM_SEED)
    numpy.random.seed(MAIN_RANDOM_SEED)
    torch.use_deterministic_algorithms(True)

