
def _get_all_gather_input_metadatas(
    param_all_gather_inputs: list[list[torch.Tensor]],
) -> tuple[list[list[torch.dtype]], list[list[int]], torch.dtype]:
    param_all_gather_input_dtypes: list[list[torch.dtype]] = []
    param_all_gather_input_numels: list[list[int]] = []
    all_gather_dtype = param_all_gather_inputs[0][0].dtype
    for all_gather_inputs in param_all_gather_inputs:
        input_dtypes: list[torch.dtype] = []
        input_numels: list[int] = []
        for all_gather_input in all_gather_inputs:
            if all_gather_input.dtype != all_gather_dtype:
                all_gather_dtype = torch.uint8
            input_dtypes.append(all_gather_input.dtype)
            input_numels.append(all_gather_input.numel())
        param_all_gather_input_dtypes.append(input_dtypes)
        param_all_gather_input_numels.append(input_numels)
    return (
        param_all_gather_input_dtypes,
        param_all_gather_input_numels,
        all_gather_dtype,
    )

