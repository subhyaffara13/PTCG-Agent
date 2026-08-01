
def offload_weight(weight: torch.Tensor, weight_name: str, offload_folder: str | None, offload_index: dict) -> dict:
    """Write `weight` to disk inside `offload_folder`, and update `offload_index` accordingly. Everything is
    saved in `safetensors` format."""

    if offload_folder is None:
        raise ValueError(
            "The current `device_map` had weights offloaded to the disk, which needed to be re-saved. This is either "
            "because the weights are not in `safetensors` format, or because the model uses an internal weight format "
            "different than the one saved (i.e. most MoE models). Please provide an `offload_folder` for them in "
            "`from_pretrained`."
        )
    # Write the weight to disk
    safetensor_file = os.path.join(offload_folder, f"{weight_name}.safetensors")
    save_file({weight_name: weight}, safetensor_file)
    # Update the offloading index
    str_dtype = str(weight.dtype).replace("torch.", "")
    offload_index[weight_name] = {"safetensors_file": safetensor_file, "weight_name": weight_name, "dtype": str_dtype}
    return offload_index

