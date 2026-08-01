
def is_local_dist_rank_0():
    return _is_torch_distributed_initialized() and int(os.environ.get("LOCAL_RANK", "-1")) == 0

