
def seed_worker(worker_id: int, num_workers: int, rank: int):
    """
    Helper function to set worker seed during Dataloader initialization.
    """
    init_seed = torch.initial_seed() % 2**32
    worker_seed = num_workers * rank + init_seed
    set_seed(worker_seed)

