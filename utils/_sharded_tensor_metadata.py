
def _sharded_tensor_metadata(
    sharded_tensor: ShardedTensor, shard_md: ShardMetadata
) -> TensorWriteData:
    shard_properties = sharded_tensor.metadata().tensor_properties

    properties = TensorProperties(
        dtype=shard_properties.dtype,
        layout=shard_properties.layout,
        requires_grad=shard_properties.requires_grad,
        memory_format=shard_properties.memory_format,
        pin_memory=shard_properties.pin_memory,
    )

    return TensorWriteData(
        chunk=_chunk_for_shard(shard_md),
        properties=properties,
        size=sharded_tensor.metadata().size,
    )

