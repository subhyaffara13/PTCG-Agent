import os

def torch_save_to_dcp(
    torch_save_path: str | os.PathLike,
    dcp_checkpoint_dir: str | os.PathLike,
):
    """
    Given the location of a torch save file, converts it into a DCP checkpoint.

    Args:
        torch_save_path: Filename of the Torch save file.
        dcp_checkpoint_dir: Directory to store the DCP checkpoint.

    .. warning::
        To avoid OOM, it's recommended to only run this function on a single rank.
    """

    state_dict = torch.load(torch_save_path, weights_only=False)
    # we don't need stateful behavior here because the expectation is anything loaded by
    # torch.load would not contain stateful objects.
    _save_state_dict(
        state_dict, storage_writer=FileSystemWriter(dcp_checkpoint_dir), no_dist=True
    )

