
def _communicate_result(result, pg):
    # Gather results from all ranks.
    if result:
        result_tensor = torch.ones(1, device=torch.device(torch.cuda.current_device()))
    else:
        result_tensor = torch.zeros(1, device=torch.device(torch.cuda.current_device()))

    dist.all_reduce(result_tensor, group=pg)

    expected_result = torch.ones(
        1, device=torch.device(torch.cuda.current_device())
    ) * dist.get_world_size(pg)

    return torch.equal(result_tensor, expected_result)

