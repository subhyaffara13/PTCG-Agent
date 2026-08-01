
def _clean_state_dict_for_safetensors(
    state_dict: dict[str, "torch.Tensor"],
    metadata: dict[str, str],
    force_contiguous: bool = True,
    shared_tensors_to_discard: list[str] | None = None,
):
    """Remove shared tensors from state_dict and update metadata accordingly (for reloading).

    Warning: `state_dict` and `metadata` are mutated in-place!

    Taken from https://github.com/huggingface/safetensors/blob/079781fd0dc455ba0fe851e2b4507c33d0c0d407/bindings/python/py_src/safetensors/torch.py#L155.
    """
    to_removes = _remove_duplicate_names(state_dict, discard_names=shared_tensors_to_discard)
    for kept_name, to_remove_group in to_removes.items():
        for to_remove in to_remove_group:
            if metadata is None:
                metadata = {}

            if to_remove not in metadata:
                # Do not override user data
                metadata[to_remove] = kept_name
            del state_dict[to_remove]
    if force_contiguous:
        state_dict = {k: v.contiguous() for k, v in state_dict.items()}
    return state_dict

