import os
from typing import Any

def load_state_dict(
    checkpoint_file: str | os.PathLike,
    map_location: str | torch.device = "cpu",
    weights_only: bool = True,
    disable_mmap: bool | None = None,
) -> dict[str, torch.Tensor]:
    """
    Reads a `safetensor` or a `.bin` checkpoint file. We load the checkpoint on "cpu" by default.

    When `disable_mmap` is True, safetensors files are read fully into memory instead of
    being memory-mapped. When `disable_mmap` is None (default), it is auto-detected to True
    on hf-mount FUSE filesystems (see `_is_on_hf_mount`).
    """
    checkpoint_path = os.fspath(checkpoint_file)
    if disable_mmap is None:
        disable_mmap = _is_on_hf_mount(checkpoint_path)
    # Use safetensors if possible
    if checkpoint_path.endswith(".safetensors"):
        if disable_mmap and map_location != "meta":
            with open(checkpoint_path, "rb") as _fh:
                state_dict = _safe_load_bytes(_fh.read())
            if map_location != "cpu":
                state_dict = {k: v.to(map_location) for k, v in state_dict.items()}
            return state_dict
        with safe_open(checkpoint_path, framework="pt") as f:
            state_dict = {}
            for k in f.keys():
                if map_location == "meta":
                    _slice = f.get_slice(k)
                    k_dtype = _slice.get_dtype()
                    if k_dtype in str_to_torch_dtype:
                        dtype = str_to_torch_dtype[k_dtype]
                    else:
                        raise ValueError(f"Cannot load safetensors of unknown dtype {k_dtype}")
                    state_dict[k] = torch.empty(size=_slice.get_shape(), dtype=dtype, device="meta")
                else:
                    state_dict[k] = f.get_tensor(k).to(map_location)
            return state_dict

    # Fallback to torch.load (if weights_only was explicitly False, do not check safety as this is known to be unsafe)
    if weights_only:
        check_torch_load_is_safe()
    extra_args = {}
    # mmap can only be used with files serialized with zipfile-based format.
    if map_location != "meta" and is_zipfile(checkpoint_path):
        extra_args = {"mmap": True}

    return torch.load(checkpoint_path, map_location=map_location, weights_only=weights_only, **extra_args)


def load_state_dict(
    state_dict: dict[str, Any],
    storage_reader: StorageReader,
    process_group: dist.ProcessGroup | None = None,
    coordinator_rank: int = 0,
    no_dist: bool = False,
    planner: LoadPlanner | None = None,
) -> None:
    """This method is deprecated. Please switch to 'load'."""
    storage_reader.reset()
    with _profile():
        # TODO: test returning `load` here instead.
        return _load_state_dict(
            state_dict,
            storage_reader,
            process_group,
            coordinator_rank,
            no_dist,
            planner,
        )

