
def load_state_dict_from_file(
    checkpoint_file: str | os.PathLike,
    map_location: Union[str, "torch.device"] | None = None,
    weights_only: bool = False,
    mmap: bool = False,
) -> dict[str, "torch.Tensor"] | Any:
    """
    Loads a checkpoint file, handling both safetensors and pickle checkpoint formats.

    Args:
        checkpoint_file (`str` or `os.PathLike`):
            Path to the checkpoint file to load. Can be either a safetensors or pickle (`.bin`) checkpoint.
        map_location (`str` or `torch.device`, *optional*):
            A `torch.device` object, string or a dict specifying how to remap storage locations. It
            indicates the location where all tensors should be loaded.
        weights_only (`bool`, *optional*, defaults to `False`):
            If True, only loads the model weights without optimizer states and other metadata.
            Only supported for pickle (`.bin`) checkpoints with PyTorch >= 1.13. Has no effect when
            loading safetensors files.
        mmap (`bool`, *optional*, defaults to `False`):
            Whether to use memory-mapped file loading. Memory mapping can improve loading performance
            for large models in PyTorch >= 2.1.0 with zipfile-based checkpoints. Has no effect when
            loading safetensors files, as the `safetensors` library uses memory mapping by default.

    Returns:
        `Union[dict[str, "torch.Tensor"], Any]`: The loaded checkpoint.
            - For safetensors files: always returns a dictionary mapping parameter names to tensors.
            - For pickle files: returns any Python object that was pickled (commonly a state dict, but could be
              an entire model, optimizer state, or any other Python object).

    Raises:
        [`FileNotFoundError`](https://docs.python.org/3/library/exceptions.html#FileNotFoundError)
            If the checkpoint file does not exist.
        [`ImportError`](https://docs.python.org/3/library/exceptions.html#ImportError)
            If safetensors or torch is not installed when trying to load a .safetensors file or a PyTorch checkpoint respectively.
        [`OSError`](https://docs.python.org/3/library/exceptions.html#OSError)
            If the checkpoint file format is invalid or if git-lfs files are not properly downloaded.
        [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError)
            If the checkpoint file path is empty or invalid.

    Example:
    ```python
    >>> from huggingface_hub import load_state_dict_from_file

    # Load a PyTorch checkpoint
    >>> state_dict = load_state_dict_from_file("path/to/model.bin", map_location="cpu")
    >>> model.load_state_dict(state_dict)

    # Load a safetensors checkpoint
    >>> state_dict = load_state_dict_from_file("path/to/model.safetensors")
    >>> model.load_state_dict(state_dict)
    ```
    """
    checkpoint_path = Path(checkpoint_file)

    # Check if file exists and is a regular file (not a directory)
    if not checkpoint_path.is_file():
        raise FileNotFoundError(
            f"No checkpoint file found at '{checkpoint_path}'. Please verify the path is correct and "
            "the file has been properly downloaded."
        )

    # Load safetensors checkpoint
    if checkpoint_path.suffix == ".safetensors":
        try:
            from safetensors import safe_open
            from safetensors.torch import load_file
        except ImportError as e:
            raise ImportError(
                "Please install `safetensors` to load safetensors checkpoint. "
                "You can install it with `pip install safetensors`."
            ) from e

        # Check format of the archive
        with safe_open(checkpoint_file, framework="pt") as f:  # type: ignore[attr-defined]
            metadata = f.metadata()
        # see comment: https://github.com/huggingface/transformers/blob/3d213b57fe74302e5902d68ed9478c3ad1aaa713/src/transformers/modeling_utils.py#L3966
        if metadata is not None and metadata.get("format") not in ["pt", "mlx"]:
            raise OSError(
                f"The safetensors archive passed at {checkpoint_file} does not contain the valid metadata. Make sure "
                "you save your model with the `save_torch_model` method."
            )
        device = str(map_location.type) if map_location is not None and hasattr(map_location, "type") else map_location
        # meta device is not supported with safetensors, falling back to CPU
        if device == "meta":
            logger.warning("Meta device is not supported with safetensors. Falling back to CPU device.")
            device = "cpu"
        return load_file(checkpoint_file, device=device)  # type: ignore[arg-type]
    # Otherwise, load from pickle
    try:
        import torch
        from torch import load
    except ImportError as e:
        raise ImportError(
            "Please install `torch` to load torch tensors. You can install it with `pip install torch`."
        ) from e
    # Add additional kwargs, mmap is only supported in torch >= 2.1.0
    additional_kwargs = {}
    if version.parse(torch.__version__) >= version.parse("2.1.0"):
        additional_kwargs["mmap"] = mmap

    # weights_only is only supported in torch >= 1.13.0
    if version.parse(torch.__version__) >= version.parse("1.13.0"):
        additional_kwargs["weights_only"] = weights_only

    return load(
        checkpoint_file,
        map_location=map_location,
        **additional_kwargs,
    )

