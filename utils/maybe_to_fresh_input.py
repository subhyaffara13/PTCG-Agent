
def maybe_to_fresh_input(idx: int, t: Any, meta: "ViewAndMutationMeta") -> Any:
    if not isinstance(t, torch.Tensor):
        return t
    if idx in meta.mutated_inp_runtime_indices:
        # We only need to bother cloning mutated inputs that participate in autograd.
        if meta.input_info[idx].requires_grad and meta.input_info[idx].mutates_data:
            # Make sure the primal we pass to autograd.grad()
            # sees the tensor before the mutation
            return t.clone()
        if meta.input_info[idx] and meta.input_info[idx].mutates_metadata:
            # Make sure the primal we pass to autograd.grad()
            # sees the tensor before the metadata mutation
            return t.view(t.shape)
    return t

