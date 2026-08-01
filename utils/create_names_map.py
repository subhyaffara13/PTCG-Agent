
def create_names_map(
    named_params: dict[str, Tensor] | Iterable[tuple[str, Tensor]],
    tied_named_params: dict[str, Tensor] | Iterable[tuple[str, Tensor]],
) -> dict[str, list[str]]:
    """
    named_params is a dictionary of tensors: {'A': A, 'B': B}
    tied_named_params is another dictionary of tensors {'A': A, 'B': B, 'B_tied': B}
    with potentially tied (or 'duplicated') tensors

    This function creates a mapping from the names in named_params to the
    names in tied_named_params: {'A': ['A'], 'B': ['B', 'B_tied']}.
    """
    named_params_dict = dict(named_params)
    tied_named_params_dict = dict(tied_named_params)

    tensors_dict_keys = set(named_params_dict.keys())
    tied_tensors_dict_keys = set(tied_named_params_dict.keys())
    if not tensors_dict_keys.issubset(tied_tensors_dict_keys):
        raise AssertionError(
            f"tensors_dict_keys {tensors_dict_keys} is not a subset of "
            f"tied_tensors_dict_keys {tied_tensors_dict_keys}"
        )

    tensor_to_mapping: dict[Tensor, tuple[str, list[str]]] = {}
    for key, tensor in named_params_dict.items():
        tensor_to_mapping[tensor] = (key, [])
    for key, tensor in tied_named_params_dict.items():
        if tensor not in tensor_to_mapping:
            raise AssertionError(
                f"tensor for key '{key}' not found in tensor_to_mapping"
            )
        tensor_to_mapping[tensor][1].append(key)
    return dict(tensor_to_mapping.values())

