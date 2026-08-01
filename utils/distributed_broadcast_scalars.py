
def distributed_broadcast_scalars(
    scalars: list[int | float],
    num_total_examples: int | None = None,
    device: torch.device | None = torch.device("cuda"),
) -> torch.Tensor:
    try:
        tensorized_scalar = torch.tensor(scalars, device=device)
        output_tensors = [tensorized_scalar.clone() for _ in range(dist.get_world_size())]
        dist.all_gather(output_tensors, tensorized_scalar)
        concat = torch.cat(output_tensors, dim=0)

        # truncate the dummy elements added by SequentialDistributedSampler
        if num_total_examples is not None:
            concat = concat[:num_total_examples]
        return concat
    except AssertionError:
        raise AssertionError("Not currently using distributed training")

