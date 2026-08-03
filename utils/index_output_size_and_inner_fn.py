import itertools

def index_output_size_and_inner_fn(
    x_size,
    indices,
    tensor_indices,
    tensor_size,
    indices_loaders,
    indexed_size,
    x_loader,
    check,
    wrap_neg=True,
):
    # Note that behavior of indexing differs when there are non consecutive
    # tensors. In this case, the tensor index is pulled to the beginning.
    #
    # Suppose a = torch.arange(3 * 4 * 5 * 6 * 7).view(3, 4, 5, 6, 7)
    #         x = torch.tensor[1,2]
    # Then, a[:,x,:,x,:] will have shape 2,3,5,7 as due to x,:,x then 2 will
    # be pulled to the front.
    non_consecutive_tensors = False
    for previous, current in itertools.pairwise(tensor_indices):
        if current - previous != 1:
            non_consecutive_tensors = True

    output_size = [x_size[i] for i, val in enumerate(indices) if val is None]
    output_size = [*output_size, *x_size[len(output_size) + len(tensor_indices) :]]

    first_tensor_index = tensor_indices[0]
    if non_consecutive_tensors:
        output_size = tensor_size + output_size
    else:
        output_size = (
            output_size[:first_tensor_index]
            + tensor_size
            + output_size[first_tensor_index:]
        )

    def fn(idx):
        assert len(idx) == len(output_size)
        assert len(indices_loaders) == len(indexed_size)

        rank = len(tensor_size)
        new_index = []
        first_tensor_index = tensor_indices[0]
        start_offset = 0 if non_consecutive_tensors else first_tensor_index
        next_idx = 0
        for i in range(tensor_indices[-1] + 1):
            if i == start_offset:
                next_idx += rank
            if indices[i] is None:
                assert next_idx < len(idx)
                new_index.append(idx[next_idx])
                next_idx += 1
            else:
                loader = indices_loaders[i]
                assert loader is not None
                size = indexed_size[i]
                new_index.append(
                    ops.indirect_indexing(
                        loader(idx[start_offset : start_offset + rank]),
                        size,
                        check=check,
                        wrap_neg=wrap_neg,
                    )
                )
        new_index = [
            *new_index,
            *idx[next_idx:],
        ]
        return new_index if x_loader is None else x_loader(new_index)

    return output_size, fn

