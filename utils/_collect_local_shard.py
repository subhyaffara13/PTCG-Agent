
def _collect_local_shard(module: torch.nn.Module) -> torch.nn.Module:
    """
    Hook a module with local shards collection in the forward pass.

    This API is typically used to convert a sharded representation back to data parallel
    representation. In particular, it returns the local tensor for this Shard. If the
    size along the sharding dimension for the local tensor is 1, this dimension is removed
    from the final result. For example a [4, 16] ShardedTensor across 4 ranks is typically
    a local Tensor of size [16] across each rank and not [1, 16] across each rank.

    Args:
        module (:class:`torch.nn.Module`): Module whose output is ShardedTensor and the
            local tensor value needs to be returned.

    Returns:
        A :class:`torch.nn.Module` object with collection API hooked.
    """

    def hook_func(_module, _input, output):
        if isinstance(output, ShardedTensor):
            local_tensor = output.local_tensor()
            # Squeeze the # of dimensions manually, only applicable to ChunkShardingSpec
            sharding_spec = output._sharding_spec
            if (
                isinstance(sharding_spec, ChunkShardingSpec)
                and local_tensor.size(sharding_spec.dim) == 1  # type: ignore[attr-defined, arg-type]
            ):
                local_tensor = local_tensor.squeeze(
                    output._sharding_spec.dim  # type: ignore[attr-defined]
                )
            return local_tensor

    module.register_forward_hook(hook_func)
    return module

