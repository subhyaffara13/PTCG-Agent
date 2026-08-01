
def get_tpu_sampler(dataset: torch.utils.data.Dataset, batch_size: int):
    if xr.world_size() <= 1:
        return RandomSampler(dataset)
    return DistributedSampler(dataset, num_replicas=xr.world_size(), rank=xr.global_ordinal())

