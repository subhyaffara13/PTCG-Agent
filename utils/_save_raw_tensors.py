
def _save_raw_tensors(
    raw_items: dict[str, tuple[torch.Tensor, TensorProperties]],
    model_name: str,
    archive_writer: PT2ArchiveWriter,
    config: dict[str, schema.PayloadMeta],
    directory: str,
    filename_prefix: str,
    idx: int,
) -> int:
    """Save deduplicated raw tensor bytes and update config. Returns updated index."""
    if not raw_items:
        return idx

    weights_dict = {model_name: Weights(raw_items)}
    storage_groups = group_weights(weights_dict)

    for group in storage_groups:
        # Find the complete tensor that covers all others in this storage group
        complete_tensor = get_complete_tensor(group, weights_dict)

        path_name = f"{filename_prefix}{idx}"
        archive_path = os.path.join(directory, path_name)
        tensor_bytes = _get_raw_tensor_bytes(complete_tensor)
        archive_writer.write_bytes(archive_path, tensor_bytes)
        idx += 1

        for _, item_fqn in group:
            tensor, _ = weights_dict[model_name].get_weight(item_fqn)
            config[item_fqn] = schema.PayloadMeta(
                path_name=path_name,
                is_param=isinstance(tensor, torch.nn.Parameter),
                use_pickle=False,
                tensor_meta=serialize_tensor_meta(tensor),
            )

    return idx

