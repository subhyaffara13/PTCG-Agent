
def _validate_keys_for_strict_loading(
    model: "torch.nn.Module",
    loaded_keys: Iterable[str],
) -> None:
    """
    Validate that model keys match loaded keys when strict loading is enabled.

    Args:
        model: The PyTorch model being loaded
        loaded_keys: The keys present in the checkpoint

    Raises:
        RuntimeError: If there are missing or unexpected keys in strict mode
    """
    loaded_keys_set = set(loaded_keys)
    model_keys = set(model.state_dict().keys())
    missing_keys = model_keys - loaded_keys_set  # Keys in model but not in checkpoint
    unexpected_keys = loaded_keys_set - model_keys  # Keys in checkpoint but not in model

    if missing_keys or unexpected_keys:
        error_message = f"Error(s) in loading state_dict for {model.__class__.__name__}"
        if missing_keys:
            str_missing_keys = ",".join([f'"{k}"' for k in sorted(missing_keys)])
            error_message += f"\nMissing key(s): {str_missing_keys}."
        if unexpected_keys:
            str_unexpected_keys = ",".join([f'"{k}"' for k in sorted(unexpected_keys)])
            error_message += f"\nUnexpected key(s): {str_unexpected_keys}."
        raise RuntimeError(error_message)

