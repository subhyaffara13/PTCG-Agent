import os
from typing import Union
from pathlib import Path


def load_torch_model(model_name, device):
    torch_model_name_or_dir = PRETRAINED_LONGFORMER_MODELS.get(model_name, model_name)
    model = LongformerModel.from_pretrained(torch_model_name_or_dir)
    model.to(device)
    return model


def load_torch_model(
    model: "torch.nn.Module",
    checkpoint_path: str | os.PathLike,
    *,
    strict: bool = False,
    safe: bool = True,
    weights_only: bool = False,
    map_location: Union[str, "torch.device"] | None = None,
    mmap: bool = False,
    filename_pattern: str | None = None,
) -> NamedTuple:
    """
    Load a checkpoint into a model, handling both sharded and non-sharded checkpoints.

    Args:
        model (`torch.nn.Module`):
            The model in which to load the checkpoint.
        checkpoint_path (`str` or `os.PathLike`):
            Path to either the checkpoint file or directory containing the checkpoint(s).
        strict (`bool`, *optional*, defaults to `False`):
            Whether to strictly enforce that the keys in the model state dict match the keys in the checkpoint.
        safe (`bool`, *optional*, defaults to `True`):
            If `safe` is True, the safetensors files will be loaded. If `safe` is False, the function
            will first attempt to load safetensors files if they are available, otherwise it will fall back to loading
            pickle files. `filename_pattern` parameter takes precedence over `safe` parameter.
        weights_only (`bool`, *optional*, defaults to `False`):
            If True, only loads the model weights without optimizer states and other metadata.
            Only supported in PyTorch >= 1.13.
        map_location (`str` or `torch.device`, *optional*):
            A `torch.device` object, string or a dict specifying how to remap storage locations. It
            indicates the location where all tensors should be loaded.
        mmap (`bool`, *optional*, defaults to `False`):
            Whether to use memory-mapped file loading. Memory mapping can improve loading performance
            for large models in PyTorch >= 2.1.0 with zipfile-based checkpoints.
        filename_pattern (`str`, *optional*):
            The pattern to look for the index file. Pattern must be a string that
            can be formatted with `filename_pattern.format(suffix=...)` and must contain the keyword `suffix`
            Defaults to `"model{suffix}.safetensors"`.
    Returns:
        `NamedTuple`: A named tuple with `missing_keys` and `unexpected_keys` fields.
            - `missing_keys` is a list of str containing the missing keys, i.e. keys that are in the model but not in the checkpoint.
            - `unexpected_keys` is a list of str containing the unexpected keys, i.e. keys that are in the checkpoint but not in the model.

    Raises:
        [`FileNotFoundError`](https://docs.python.org/3/library/exceptions.html#FileNotFoundError)
            If the checkpoint file or directory does not exist.
        [`ImportError`](https://docs.python.org/3/library/exceptions.html#ImportError)
            If safetensors or torch is not installed when trying to load a .safetensors file or a PyTorch checkpoint respectively.
        [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError)
           If the checkpoint path is invalid or if the checkpoint format cannot be determined.

    Example:
    ```python
    >>> from huggingface_hub import load_torch_model
    >>> model = ... # A PyTorch model
    >>> load_torch_model(model, "path/to/checkpoint")
    ```
    """
    checkpoint_path = Path(checkpoint_path)

    if not checkpoint_path.exists():
        raise ValueError(f"Checkpoint path {checkpoint_path} does not exist")
    # 1. Check if checkpoint is a single file
    if checkpoint_path.is_file():
        state_dict = load_state_dict_from_file(
            checkpoint_file=checkpoint_path,
            map_location=map_location,
            weights_only=weights_only,
        )
        return model.load_state_dict(state_dict, strict=strict)

    # 2. If not, checkpoint_path is a directory
    if filename_pattern is None:
        filename_pattern = constants.SAFETENSORS_WEIGHTS_FILE_PATTERN
        index_path = checkpoint_path / (filename_pattern.format(suffix="") + ".index.json")
        # Only fallback to pickle format if safetensors index is not found and safe is False.
        if not index_path.is_file() and not safe:
            filename_pattern = constants.PYTORCH_WEIGHTS_FILE_PATTERN

    index_path = checkpoint_path / (filename_pattern.format(suffix="") + ".index.json")

    if index_path.is_file():
        return _load_sharded_checkpoint(
            model=model,
            save_directory=checkpoint_path,
            strict=strict,
            weights_only=weights_only,
            filename_pattern=filename_pattern,
        )

    # Look for single model file
    model_files = list(checkpoint_path.glob("*.safetensors" if safe else "*.bin"))
    if len(model_files) == 1:
        state_dict = load_state_dict_from_file(
            checkpoint_file=model_files[0],
            map_location=map_location,
            weights_only=weights_only,
            mmap=mmap,
        )
        return model.load_state_dict(state_dict, strict=strict)

    raise ValueError(
        f"Directory '{checkpoint_path}' does not contain a valid checkpoint. "
        "Expected either a sharded checkpoint with an index file, or a single model file."
    )

