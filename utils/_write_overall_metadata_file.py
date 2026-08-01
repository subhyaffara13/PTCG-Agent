
def _write_overall_metadata_file(
    output_dir: str,
    output_files_data: dict[str, _OutputFileData],
) -> None:
    """
    Write the overall metadata file that maps tensor names to their file locations.

    This creates a model.safetensors.index.json file that HuggingFace models use
    to locate tensors across multiple files.

    Args:
        output_dir: Directory where the metadata file will be written
        output_files_data: Dictionary mapping output file paths to their metadata
    """
    total_size = 0
    weight_map = {}
    for output_path, value in output_files_data.items():
        for fqn, fqn_data in value.fqn_data.items():
            total_size += math.prod(fqn_data.shape_in_file) * fqn_data.dtype_size
            weight_map[fqn] = os.path.basename(output_path)

    metadata_to_write: dict[str, Any] = {}
    metadata_to_write["metadata"] = {"total_size": total_size}
    metadata_to_write["weight_map"] = weight_map

    metadata_path = os.path.join(output_dir, f"{_metadata_fn}")
    with open(metadata_path, "w") as metadata_file:
        json.dump(metadata_to_write, metadata_file, indent=2)

