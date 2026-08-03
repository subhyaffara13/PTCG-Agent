import os
from typing import Any

def _load_state_dict_from_keys(
    keys: set[str] | str | None = None,
    *,
    checkpoint_id: str | os.PathLike | None = None,
    storage_reader: StorageReader | None = None,
    process_group: dist.ProcessGroup | None = None,
) -> dict[str, Any]:
    """
    Load only the specified keys from the checkpoint, if no keys are specified, the entire
    checkpoint will be loaded. Note, this method completely loads the checkpoint into the
    current process and is not distributed.

    .. warning::


    .. warning::

        All non-tensor data is loaded using `torch.load()`

    .. note:
        As opposed to the usual pattern, this function does not take a state dict as input
        and does not load inplace. Instead, a new state dict is directly initialized and read
        from file.

    .. note:
        If no process group is initialized, this function will assume the intent
        is to load a checkpoint into the local process. This can be useful in the
        case of local inference, and when using regular Tensors (as opposed to DTensor
         or ShardedTensor)

    .. note:
        Rank 0 is assumed to be the coordinator rank.

    Args:
        keys (Optional[Union[set[str], str]]):
            Loads any key specified in this set. If no keys are specified, the entire checkpoint
            is loaded.
        checkpoint_id (Union[str, os.PathLike, None]):
            The ID of this checkpoint instance. The meaning of the checkpoint_id
            depends on the storage. It can be a path to a folder or to a file.
            It can also be a key if the storage is a key-value store.
            (Default: ``None``)
        storage_reader (Optional[StorageReader]):
            Instance of StorageWriter used to perform reads. If this is not
            specified, DCP will automatically infer the reader based on the
            checkpoint_id. If checkpoint_id is also None, an exception will
            be raised. (Default: ``None``)
        process_group (Optional[ProcessGroup]):
            ProcessGroup to be used for cross-rank synchronization.
            (Default: ``None``)

    Returns:
        State dict from specified keys
    """
    torch._C._log_api_usage_once(
        "torch.distributed.checkpoint._load_state_dict_from_keys"
    )

    no_dist = not (dist.is_available() and dist.is_initialized())
    if no_dist:
        warnings.warn(
            "torch.distributed is unavailable or uninitialized, assuming the intent is to load in a single process.",
            stacklevel=2,
        )

    storage_reader = cast(
        StorageReader, _storage_setup(storage_reader, checkpoint_id, reader=True)
    )

    if isinstance(keys, str):
        keys = {keys}

    sd: dict[str, Any] = {}
    _load_state_dict(
        state_dict=sd,
        storage_reader=storage_reader,
        process_group=process_group,
        no_dist=no_dist,
        planner=_EmptyStateDictLoadPlanner(keys=keys),
    )

    return sd

