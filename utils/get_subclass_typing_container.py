
def get_subclass_typing_container(
    tensor_subclass: torch.Tensor,
) -> dict[type[torch.Tensor], list[type[torch.Tensor]]]:
    """
    Given a subclass, returns a recursive dictionary mapping each
    inner tensors to its' subclass types.
    """

    def _get_types_for_subclass(tensor_subclass: torch.Tensor) -> None:
        if not is_traceable_wrapper_subclass(tensor_subclass):
            return
        tracker[type(tensor_subclass)].append(tensor_subclass)
        inner_keys, _ = tensor_subclass.__tensor_flatten__()
        for key in inner_keys:
            match getattr(tensor_subclass, key):
                case torch.Tensor() as inner_value:
                    _get_types_for_subclass(inner_value)
                case OpaqueBase():
                    pass
                case unexpected:
                    raise AssertionError(
                        f"expected Tensor or OpaqueBase, got {type(unexpected)}"
                    )

    tracker: dict[Any, list[Any]] = collections.defaultdict(list)
    _get_types_for_subclass(tensor_subclass)
    return tracker

