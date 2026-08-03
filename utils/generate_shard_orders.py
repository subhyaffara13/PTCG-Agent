import itertools

def generate_shard_orders(mesh, tensor_rank):
    # Generate all possible sharding placement of tensor with rank
    # `tensor_rank` over mesh.
    def _split_list(lst: list, N: int):
        def compositions(n: int, k: int):
            # yields lists of length k, positive ints summing to n
            for cuts in itertools.combinations(range(1, n), k - 1):
                # add 0 and n as sentinels, then take consecutive differences
                yield [b - a for a, b in itertools.pairwise((0, *cuts, n))]

        length = len(lst)
        for comp in compositions(length, N):
            result = []
            start = 0
            for size in comp:
                result.append(lst[start : start + size])
                start += size
            yield result

    all_mesh = list(range(mesh.ndim))
    all_device_order = list(itertools.permutations(all_mesh))
    for device_order in all_device_order:
        # split on device orders, and assign each device order segment to a tensor dim
        for num_split in range(1, mesh.ndim + 1):
            for splitted_list in _split_list(list(range(mesh.ndim)), num_split):
                for tensor_dims in itertools.combinations(
                    range(tensor_rank), len(splitted_list)
                ):
                    shard_order = {}
                    if len(tensor_dims) != len(splitted_list):
                        raise AssertionError(
                            f"Expected len(tensor_dims) == len(splitted_list), "
                            f"got {len(tensor_dims)} != {len(splitted_list)}"
                        )
                    for tensor_dim, mesh_dims in zip(tensor_dims, splitted_list):
                        shard_order[tensor_dim] = device_order[
                            mesh_dims[0] : mesh_dims[-1] + 1
                        ]
                    yield _convert_shard_order_dict_to_ShardOrder(shard_order)

