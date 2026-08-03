import json
import os
from pathlib import Path


def _load_sharded_checkpoint(
    model: "torch.nn.Module",
    save_directory: os.PathLike,
    *,
    strict: bool = False,
    weights_only: bool = False,
    filename_pattern: str = constants.SAFETENSORS_WEIGHTS_FILE_PATTERN,
) -> NamedTuple:
    """
    Loads a sharded checkpoint into a model. This is the same as
    [`torch.nn.Module.load_state_dict`](https://pytorch.org/docs/stable/generated/torch.nn.Module.html?highlight=load_state_dict#torch.nn.Module.load_state_dict)
    but for a sharded checkpoint. Each shard is loaded one by one and removed from memory after being loaded into the model.

    Args:
        model (`torch.nn.Module`):
            The model in which to load the checkpoint.
        save_directory (`str` or `os.PathLike`):
            A path to a folder containing the sharded checkpoint.
        strict (`bool`, *optional*, defaults to `False`):
            Whether to strictly enforce that the keys in the model state dict match the keys in the sharded checkpoint.
        weights_only (`bool`, *optional*, defaults to `False`):
            If True, only loads the model weights without optimizer states and other metadata.
            Only supported in PyTorch >= 1.13.
        filename_pattern (`str`, *optional*, defaults to `"model{suffix}.safetensors"`):
            The pattern to look for the index file. Pattern must be a string that
            can be formatted with `filename_pattern.format(suffix=...)` and must contain the keyword `suffix`
            Defaults to `"model{suffix}.safetensors"`.

    Returns:
        `NamedTuple`: A named tuple with `missing_keys` and `unexpected_keys` fields,
            - `missing_keys` is a list of str containing the missing keys
            - `unexpected_keys` is a list of str containing the unexpected keys
    """

    # 1. Load and validate index file
    # The index file contains mapping of parameter names to shard files
    index_path = filename_pattern.format(suffix="") + ".index.json"
    index_file = os.path.join(save_directory, index_path)
    with open(index_file, encoding="utf-8") as f:
        index = json.load(f)

    # 2. Validate shard filenames from the index
    # This prevents path traversal attacks and extension confusion attacks
    # (e.g. a safetensors index referencing .bin pickle files)
    expected_extension = Path(filename_pattern.format(suffix="")).suffix  # e.g. ".safetensors"
    shard_files = list(set(index["weight_map"].values()))
    for shard_file in shard_files:
        # Reject anything that could escape `save_directory` on any host OS:
        # POSIX absolute ("/tmp/x"), Windows drive ("C:x", "C:\\x"), UNC
        # ("\\\\server\\share\\x"), rooted-without-drive ("\\x", "/x"), or
        # ".." traversal — including "..\\x" which `os.path.isabs` never caught on POSIX.
        #
        # We parse with `PureWindowsPath` *regardless of host OS*: it treats both "/" and
        # "\\" as separators and exposes `drive` / `root`, so a single check rejects a
        # malicious index file on Linux too (e.g. if it's later opened on Windows). The
        # only over-strict case is a POSIX filename like "a:foo" which would be parsed as
        # drive "a:" — such names are never produced for safetensors shards and would
        # break on Windows anyway, so rejecting them is fine.
        win_path = PureWindowsPath(shard_file)
        if win_path.drive or win_path.root or ".." in win_path.parts:
            raise ValueError(
                f"Invalid shard filename '{shard_file}' in index file '{index_file}'. "
                "Shard filenames must be relative paths without '..' components."
            )
        # Reject extension mismatch (e.g. .bin shard in a .safetensors index)
        if not shard_file.endswith(expected_extension):
            raise ValueError(
                f"Invalid shard filename '{shard_file}' in index file '{index_file}'. "
                f"Expected '{expected_extension}' extension to match the index format."
            )

    # 3. Validate keys if in strict mode
    # This is done before loading any shards to fail fast
    if strict:
        _validate_keys_for_strict_loading(model, index["weight_map"].keys())

    # 4. Load each shard using `load_state_dict`
    # Get unique shard files (multiple parameters can be in same shard)
    for shard_file in shard_files:
        # Load shard into memory
        shard_path = os.path.join(save_directory, shard_file)
        state_dict = load_state_dict_from_file(
            shard_path,
            map_location="cpu",
            weights_only=weights_only,
        )
        # Update model with parameters from this shard
        model.load_state_dict(state_dict, strict=strict)
        # Explicitly remove the state dict from memory
        del state_dict

    # 5. Return compatibility info
    loaded_keys = set(index["weight_map"].keys())
    model_keys = set(model.state_dict().keys())
    return _IncompatibleKeys(
        missing_keys=list(model_keys - loaded_keys), unexpected_keys=list(loaded_keys - model_keys)
    )

