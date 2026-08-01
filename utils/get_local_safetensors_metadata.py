
def get_local_safetensors_metadata(path: str | Path) -> SafetensorsRepoMetadata:
    """
    Parse metadata for a local safetensors file or folder.

    Supports:
    - Single safetensors file (e.g., `model.safetensors`)
    - Directory with non-sharded model (contains `model.safetensors`)
    - Directory with sharded model (contains `model.safetensors.index.json`)

    For more details regarding the safetensors format, check out https://huggingface.co/docs/safetensors/index#format.

    Args:
        path (`str` or `Path`):
            Path to a safetensors file or directory containing safetensors files.

    Returns:
        [`SafetensorsRepoMetadata`]: information related to the safetensors repo.

    Raises:
        [`NotASafetensorsRepoError`]:
            If the path is not a valid safetensors file or folder (i.e., doesn't have either a
            `model.safetensors` or a `model.safetensors.index.json` file).
        [`SafetensorsParsingError`]:
            If a safetensors file header couldn't be parsed correctly.
        `FileNotFoundError`:
            If the path does not exist.

    Example:
        ```py
        # Parse single safetensors file
        >>> metadata = get_local_safetensors_metadata("path/to/model.safetensors")
        >>> metadata
        SafetensorsRepoMetadata(metadata=None, sharded=False, weight_map={...}, files_metadata={...})

        # Parse directory with sharded model
        >>> metadata = get_local_safetensors_metadata("path/to/model_folder")
        >>> metadata
        SafetensorsRepoMetadata(metadata={'total_size': ...}, sharded=True, weight_map={...}, files_metadata={...})
        >>> len(metadata.files_metadata)
        3  # Number of safetensors shards
        ```
    """
    path = Path(path)

    # Case 1: Direct path to a safetensors file
    if path.is_file():
        file_metadata = parse_local_safetensors_file_metadata(path)
        return SafetensorsRepoMetadata(
            metadata=None,
            sharded=False,
            weight_map={tensor_name: path.name for tensor_name in file_metadata.tensors.keys()},
            files_metadata={path.name: file_metadata},
        )

    # Case 2: Directory
    if not path.is_dir():
        raise FileNotFoundError(f"Path '{path}' does not exist.")

    single_file_path = path / constants.SAFETENSORS_SINGLE_FILE
    index_file_path = path / constants.SAFETENSORS_INDEX_FILE

    # Case 2a: Non-sharded model (single model.safetensors file)
    if single_file_path.exists():
        file_metadata = parse_local_safetensors_file_metadata(single_file_path)
        return SafetensorsRepoMetadata(
            metadata=None,
            sharded=False,
            weight_map={
                tensor_name: constants.SAFETENSORS_SINGLE_FILE for tensor_name in file_metadata.tensors.keys()
            },
            files_metadata={constants.SAFETENSORS_SINGLE_FILE: file_metadata},
        )

    # Case 2b: Sharded model (model.safetensors.index.json)
    if index_file_path.exists():
        with open(index_file_path) as f:
            index = json.load(f)

        weight_map = index.get("weight_map", {})

        # Parse metadata from each shard
        files_metadata = {}
        for shard_filename in set(weight_map.values()):
            shard_path = path / shard_filename
            files_metadata[shard_filename] = parse_local_safetensors_file_metadata(shard_path)

        return SafetensorsRepoMetadata(
            metadata=index.get("metadata", None),
            sharded=True,
            weight_map=weight_map,
            files_metadata=files_metadata,
        )

    # Not a valid safetensors folder
    raise NotASafetensorsRepoError(
        f"'{path}' is not a valid safetensors folder. Couldn't find '{constants.SAFETENSORS_INDEX_FILE}' or "
        f"'{constants.SAFETENSORS_SINGLE_FILE}' files."
    )

