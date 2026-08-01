
def tensor_requires_grad_set(types, args=(), kwargs=None, pg=None):
    # pyrefly: ignore [bad-index]
    self_st = args[0]
    # Validate types
    if not isinstance(self_st, ShardedTensor):
        raise TypeError("input needs to be a ShardedTensor")

    if kwargs is None:
        kwargs = {}

    requires_grad = args[1] if len(args) > 1 else kwargs.get("requires_grad", True)
    if requires_grad == self_st.requires_grad:
        return self_st

    for local_shard in self_st.local_shards():
        local_shard.tensor.requires_grad_(requires_grad)

        # update the wrapper class property
    with torch._C.DisableTorchFunctionSubclass():
        self_st.requires_grad_(requires_grad)
    # update the metadata in the meanwhile
    self_st._metadata.tensor_properties.requires_grad = requires_grad
    return self_st

