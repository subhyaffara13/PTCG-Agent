
def _print_nested(
    value: STATE_DICT_ITEM,
    prefix: str = "",
    print_fun: Callable[[str], None] = print,
) -> None:
    if type(value) is ShardedTensor:
        print_fun(f"{prefix} ShardedTensor size: {value.size()}")
        for shard in value.local_shards():
            _print_nested(
                shard.tensor,
                f"{shard.metadata.shard_offsets} ",
                print_fun=print_fun,
            )
    elif type(value) is (DTensor):
        print_fun(f"{prefix} DistributedTensor size: {value.size()}")
        # TODO: add local offset for _local_tensor in print_nested.
        _print_nested(
            value._local_tensor,
            print_fun=print_fun,
        )
    elif isinstance(value, torch.Tensor):
        print_fun(f"{prefix} Tensor size: {value.size()}")
    else:
        print_fun(f"{prefix} Type: {type(value)}")

