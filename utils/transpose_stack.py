
def transpose_stack(
    tuple_of_tuple_of_tensors: tuple[tuple[Tensor, ...], ...],
) -> tuple[Tensor, ...]:
    tuple_of_tuple_of_tensors = tuple(zip(*tuple_of_tuple_of_tensors))
    results = tuple(
        torch.stack(shards).detach() for shards in tuple_of_tuple_of_tensors
    )
    return results

