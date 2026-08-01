
def copy_slices_epilogue(
    needs_input_grad: Sequence[bool],
    result: torch.Tensor,
    res: Sequence[torch.Tensor | None],
    grad_slice: torch.Tensor,
) -> list[torch.Tensor | None]:
    grad_inputs: list[torch.Tensor | None] = [None] * len(needs_input_grad)
    for i in range(len(needs_input_grad)):
        if needs_input_grad[i]:
            if res[i] is None:
                continue
            if i == 0:
                to_copy = res[i]
                assert to_copy is not None
                grad_slice.copy_(to_copy)
                grad_inputs[i] = result
            else:
                grad_inputs[i] = res[i]
    return grad_inputs

