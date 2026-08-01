
def requires_ddp_rank(device):
    return device in DDP_RANK_DEVICES

