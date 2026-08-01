
def _serialize_tensor_like_io(
    value, debug_path: str | None = None, use_repr: bool = True, path_to_value: str | None = None
):
    """
    Converts Tensors and DTensors to a JSON-serializable dictionary representation.

    Args:
        value: Any Python object, often including torch Tensors, lists, dicts, etc.
        debug_path (`str`, *optional*, defaults to `None`): Directory to dump debug JSON and SafeTensors files.
        use_repr (bool, *optional*, defaults to `True`): Whether to save a `repr()`-ized version of the tensor as the
            `value` property in the asscoiated FULL_TENSORS.json file, or to store the full tensors in separate
            SafeTensors file and store the relative path to that file in the `value` property in the dictionary.
        path_to_value (`str`, *optional*, defaults to `None`): The file name for the SafeTensors file holding the full
            tensor value if `use_repr=False`.

    Returns:
        A nested Python structure (list, dict, or sanitized string) that is safe to json.dump.
    """
    torch.set_printoptions(sci_mode=True)

    if use_repr:
        value_out = _repr_to_list(value)
    elif path_to_value:
        if not path_to_value.endswith(".safetensors"):
            path_to_value += ".safetensors"

        filepath = os.path.join(debug_path, path_to_value) if debug_path else path_to_value
        save_file({"data": value.contiguous().detach().cpu()}, filepath)
        value_out = f"./{path_to_value}"
    else:
        raise ValueError(f"{use_repr=} and {path_to_value=} cannot both be falsy.")

    out = {
        "shape": repr(value.shape),
        "dtype": repr(value.dtype),
        "value": value_out,
    }
    if value.dtype in {torch.float16, torch.float32, torch.bfloat16}:
        out.update(
            {
                "mean": _sanitize_repr_for_diff(repr(value.mean())),
                "std": _sanitize_repr_for_diff(repr(value.std())),
                "min": _sanitize_repr_for_diff(repr(value.min())),
                "max": _sanitize_repr_for_diff(repr(value.max())),
            }
        )
    return out

