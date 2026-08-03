import os

def _save_pickled_tensors(
    pickled_items: list[tuple[str, torch.Tensor]],
    archive_writer: PT2ArchiveWriter,
    config: dict[str, schema.PayloadMeta],
    directory: str,
    filename_prefix: str,
    idx: int,
    pickle_protocol: int = DEFAULT_PICKLE_PROTOCOL,
) -> int:
    """Save pickled tensors and update config. Returns updated index."""
    for item_fqn, tensor in pickled_items:
        path_name = f"{filename_prefix}{idx}"
        archive_path = os.path.join(directory, path_name)
        buffer = io.BytesIO()
        torch.save(tensor, buffer, pickle_protocol=pickle_protocol)
        archive_writer.write_bytes(archive_path, buffer.getvalue())

        config[item_fqn] = schema.PayloadMeta(
            path_name=path_name,
            is_param=isinstance(tensor, torch.nn.Parameter),
            use_pickle=True,
            tensor_meta=serialize_tensor_meta(tensor),
        )
        idx += 1
    return idx

