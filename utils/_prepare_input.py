
def _prepare_input(
    input: torch.Tensor, maybe_perturbed_input: torch.Tensor | None, fast_mode=False
) -> torch.Tensor:
    # Prepares the inputs to be passed into the function while including the new
    # modified input.
    if input.layout == torch._mkldnn:  # type: ignore[attr-defined] # no attr _mkldnn
        # Convert back to mkldnn
        if maybe_perturbed_input is not None:
            return maybe_perturbed_input.to_mkldnn()
        else:
            return input
    elif _is_sparse_any_tensor(input):
        if fast_mode and maybe_perturbed_input is not None:
            # entry is already a "cloned" version of the original tensor
            # thus changes to entry are not reflected in the input
            return maybe_perturbed_input
        else:
            return input
    else:
        # We cannot use entry (input.data) if we want gradgrad to work because
        # fn (in the gradgrad case) needs to compute grad wrt input
        return input

