
def patch_reshard(new_reshard: Callable):
    orig_reshard = FSDPParamGroup.reshard
    dist.barrier()
    FSDPParamGroup.reshard = new_reshard
    try:
        yield
    finally:
        dist.barrier()
        FSDPParamGroup.reshard = orig_reshard

