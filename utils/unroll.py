import math


def unroll(
    hidden_states: torch.Tensor, image_shape: tuple[int, int], patch_stride: tuple[int, int], schedule: list[list[int]]
) -> torch.Tensor:
    """
    Reorders the tokens such that patches are contiguous in memory.
    E.g., given [batch_size, (height, width), hidden_size] and stride of (stride, stride), this will re-order the tokens as
    [batch_size, (stride, stride, height // stride, width // stride), hidden_size]

    This allows operations like Max2d to be computed as x.view(batch_size, stride*stride, -1, hidden_size).max(dim=1).
    Not only is this faster, but it also makes it easy to support inputs of arbitrary
    dimensions in addition to patch-wise sparsity.

    Performing this operation multiple times in sequence puts entire windows as contiguous
    in memory. For instance, if you applied the stride (2, 2) 3 times, entire windows of
    size 8x8 would be contiguous in memory, allowing operations like mask unit attention
    computed easily and efficiently, while also allowing max to be applied sequentially.

    Note: This means that intermediate values of the model are not in height x width order, so they
    need to be re-rolled if you want to use the intermediate values as a height x width feature map.
    The last block of the network is fine though, since by then the strides are all consumed.
    """
    batch_size, _, hidden_size = hidden_states.shape

    size = [i // s for i, s in zip(image_shape, patch_stride)]

    current_size = size
    hidden_states = hidden_states.view(*([batch_size] + current_size + [hidden_size]))

    for strides in schedule:
        # Move patches with the given strides to the batch dimension

        # Create a view of the tensor with the patch stride as separate dims
        # For example in 2d: [batch_size, height // stride, stride, width // stride, stride, C]
        current_size = [i // s for i, s in zip(current_size, strides)]
        # initialize new_shape with [height // stride, stride, width // stride, stride]
        new_shape = [item for pair in zip(current_size, strides) for item in pair]
        # add batch_size and hidden_size to new_shape
        new_shape = [batch_size] + new_shape + [hidden_size]
        hidden_states = hidden_states.view(new_shape)

        # Move the patch stride into the batch dimension
        # For example in 2d: [batch_size, stride, stride, height // stride, width // stride, hidden_size]
        num_dims = len(new_shape)
        permute = [0] + list(range(2, num_dims - 1, 2)) + list(range(1, num_dims - 1, 2)) + [num_dims - 1]
        hidden_states = hidden_states.permute(permute)

        # Now finally flatten the relevant dims into the batch dimension
        hidden_states = hidden_states.flatten(0, len(strides))
        batch_size *= math.prod(strides)

    hidden_states = hidden_states.reshape(-1, math.prod(size), hidden_size)
    return hidden_states

