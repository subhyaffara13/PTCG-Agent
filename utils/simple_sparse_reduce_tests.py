
def simple_sparse_reduce_tests(rank: int, world_size: int, num_inputs: int = 1):
    """
    Generate a number of basic test cases for sparse reduction.
    These cover tensors with a varying number of sparse dimensions and a varying
    number of dense dimensions. The only reduction operation we support is sum.
    """

    def generate(rank: int, world_size: int, sparse_dims: int = 1, dense_dims: int = 0):
        # First sparse dimension is [0..rank].
        # Subsequent dimensions are always 0, so we know there is
        # a non-empty intersection between any two sparse tensors.
        indices = torch.reshape(torch.arange(rank + 1), (1, rank + 1))
        shape = [world_size] + [2 for _ in range(dense_dims)]
        for _ in range(sparse_dims - 1):
            indices = torch.cat((indices, torch.zeros(1, rank + 1)))
            shape.append(world_size)
        values = torch.ones([rank + 1] + [2 for _ in range(dense_dims)])
        return torch.sparse_coo_tensor(indices, values, shape)

    def compute_sum(fn, world_size: int):
        return reduce(
            operator.add, [fn(rank, world_size) for rank in range(world_size)]
        )

    return [
        (
            [
                fn(num_inputs * rank + i, num_inputs * world_size)
                for i in range(num_inputs)
            ],
            [compute_sum(fn, num_inputs * world_size) for i in range(num_inputs)],
        )
        for fn in [
            partial(generate, sparse_dims=1),
            partial(generate, sparse_dims=2),
            partial(generate, sparse_dims=3),
            partial(generate, dense_dims=1),
            partial(generate, dense_dims=2),
            partial(generate, dense_dims=3),
        ]
    ]

