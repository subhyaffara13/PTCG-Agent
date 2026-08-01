
def _serialize_io(value, debug_path: str | None = None, use_repr: bool = True, path_to_value: str | None = None):
    """
    Recursively build a JSON-serializable Python structure from `value`.
    Tensors and DTensors become either sanitized repr strings, or are saved to disk as SafeTensors files and their
    relative paths are recorded in the returned Python structure.
    Lists/tuples/dicts are recursed into.
    All memory addresses are replaced with a stable placeholder.

    Args:
        value: Any Python object, often including torch Tensors, lists, dicts, etc.
        debug_path (`str`, *optional*, defaults to `None`): Directory to dump debug JSON and SafeTensors files.
        use_repr (bool, *optional*, defaults to `True`): Whether to save a `repr()`-ized version of the tensors as the
            `value` property in the asscoiated FULL_TENSORS.json file, or to store full tensors in separate SafeTensors
            files and store the relative path to that file in the `value` property.
        path_to_value (`str`, *optional*, defaults to `None`): The file name for the SafeTensors file holding the full
            tensor value if `use_repr=False`.

    Returns:
        A nested Python structure (list, dict, or sanitized string) that is safe to json.dump.
    """
    if isinstance(value, (list, tuple)):
        return [
            _serialize_io(v, debug_path=debug_path, use_repr=use_repr, path_to_value=f"{path_to_value}_{i}")
            for i, v in enumerate(value)
        ]

    if isinstance(value, dict):
        return {
            k: _serialize_io(v, debug_path=debug_path, use_repr=use_repr, path_to_value=f"{path_to_value}_{k}")
            for k, v in value.items()
        }

    if hasattr(value, "_local_tensor"):
        return _serialize_tensor_like_io(
            value._local_tensor, debug_path=debug_path, use_repr=use_repr, path_to_value=path_to_value
        )

    if isinstance(value, torch.Tensor):
        return _serialize_tensor_like_io(value, debug_path=debug_path, use_repr=use_repr, path_to_value=path_to_value)

    return _sanitize_repr_for_diff(repr(value))

