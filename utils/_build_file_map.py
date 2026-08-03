import os

def _build_file_map(
    archive_reader: PT2ArchiveReader,
    config: schema.PayloadConfig,
    base_dir: str,
) -> dict[str, torch.Tensor]:
    """
    Build a map from file path to the payload in flat tensor format.
    """
    file_map: dict[str, torch.Tensor] = {}
    for payload_meta in config.config.values():
        # skip pickled objects
        if payload_meta.use_pickle:
            continue
        # skip files that already exist in the map
        if payload_meta.path_name in file_map:
            continue

        tensor_bytes = archive_reader.read_bytes(
            os.path.join(base_dir, payload_meta.path_name)
        )
        if payload_meta.tensor_meta is None:
            raise AssertionError("payload_meta.tensor_meta cannot be None")
        tensor = _create_flat_tensor_from_bytes(tensor_bytes, payload_meta.tensor_meta)
        file_map[payload_meta.path_name] = tensor

    return file_map

