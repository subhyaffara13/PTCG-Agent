
def _convert_shard_order_dict_to_ShardOrder(shard_order):
    """Convert shard_order dict to ShardOrder"""
    return tuple(
        ShardOrderEntry(tensor_dim=tensor_dim, mesh_dims=tuple(mesh_dims))
        for tensor_dim, mesh_dims in shard_order.items()
    )

