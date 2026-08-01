
def bucket_key(node: torch.fx.Node, mode: BucketMode | None = None) -> object | None:
    if is_all_gather_into_tensor(node):
        group_key_fn = (
            _ag_group_key_multidtype if mode and "multidtype" in mode else _ag_group_key
        )
        return group_key_fn(node)
    elif is_reduce_scatter_tensor(node):
        return _rs_group_key(node)
    elif is_all_reduce_tensor(node):
        return _ar_group_key(node)
    else:
        return None

