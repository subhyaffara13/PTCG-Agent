
def is_channels_last(ten):
    return torch._prims_common.suggest_memory_format(ten) == torch.channels_last

