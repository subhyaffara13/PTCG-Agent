import os

def _package_state_dict(
    model_name: str,
    exported_program: ExportedProgram,
    archive_writer: PT2ArchiveWriter,
    pickle_protocol: int = DEFAULT_PICKLE_PROTOCOL,
) -> schema.PayloadConfig:
    weights_config: dict[str, schema.PayloadMeta] = {}

    pickled_weights: list[tuple[str, torch.Tensor]] = []
    raw_weights: dict[str, tuple[torch.Tensor, TensorProperties]] = {}

    # Categorize weights
    for weight_fqn, weight_tensor in exported_program.state_dict.items():
        if not isinstance(weight_tensor, torch.Tensor):
            raise AssertionError("only torch.Tensor is allowed in state_dict")
        if _should_use_pickle(weight_tensor):
            pickled_weights.append((weight_fqn, weight_tensor))
        else:
            raw_weights[weight_fqn] = (weight_tensor, TensorProperties(weight_tensor))

    idx = archive_writer.count_prefix(os.path.join(WEIGHTS_DIR, WEIGHT_FILENAME_PREFIX))

    # Save weights in pickle format
    idx = _save_pickled_tensors(
        pickled_weights,
        archive_writer,
        weights_config,
        WEIGHTS_DIR,
        WEIGHT_FILENAME_PREFIX,
        idx,
        pickle_protocol,
    )

    # Save weights in raw bytes format
    _save_raw_tensors(
        raw_weights,
        model_name,
        archive_writer,
        weights_config,
        WEIGHTS_DIR,
        WEIGHT_FILENAME_PREFIX,
        idx,
    )

    return schema.PayloadConfig(config=weights_config)

