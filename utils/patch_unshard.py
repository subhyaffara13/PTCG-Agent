
def patch_unshard(new_unshard: Callable):
    orig_unshard = FSDPParamGroup.unshard
    dist.barrier()
    FSDPParamGroup.unshard = new_unshard
    try:
        yield
    finally:
        dist.barrier()
        FSDPParamGroup.unshard = orig_unshard

