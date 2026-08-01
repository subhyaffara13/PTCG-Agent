
def tensor_device(types, args=(), kwargs=None, pg=None):
    # pyrefly: ignore [bad-index]
    self_st = args[0]
    # Validate types
    if not isinstance(self_st, ShardedTensor):
        raise TypeError("input needs to be a ShardedTensor")
    dev: torch.device
    if self_st._local_shards:
        dev = self_st._local_shards[0].tensor.device
    elif pg and pg._get_backend_name() == "gloo":
        dev = torch.device("cpu")
    else:
        dev = torch.device(torch.cuda.current_device())
    return dev

