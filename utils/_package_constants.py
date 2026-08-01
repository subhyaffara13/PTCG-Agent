
def _package_constants(
    model_name: str,
    exported_program: ExportedProgram,
    archive_writer: PT2ArchiveWriter,
    pickle_protocol: int = DEFAULT_PICKLE_PROTOCOL,
) -> schema.PayloadConfig:
    constants_config: dict[str, schema.PayloadMeta] = {}

    pickled_constants: list[tuple[str, torch.Tensor]] = []
    raw_constants: dict[str, tuple[torch.Tensor, TensorProperties]] = {}
    custom_objects: list[tuple[str, torch._C.ScriptObject]] = []

    # Categorize constants
    for constant_fqn, constant in exported_program.constants.items():
        if isinstance(constant, torch.Tensor):
            if _should_use_pickle(constant):
                pickled_constants.append((constant_fqn, constant))
            else:
                raw_constants[constant_fqn] = (constant, TensorProperties(constant))

        elif isinstance(constant, torch._C.ScriptObject):
            custom_objects.append((constant_fqn, constant))

        else:
            raise RuntimeError(f"Unsupported constant type: {type(constant)}")

    tensor_idx = archive_writer.count_prefix(
        os.path.join(CONSTANTS_DIR, TENSOR_CONSTANT_FILENAME_PREFIX)
    )
    custom_obj_idx = archive_writer.count_prefix(
        os.path.join(CONSTANTS_DIR, CUSTOM_OBJ_FILENAME_PREFIX)
    )

    # Save constants in pickle format
    tensor_idx = _save_pickled_tensors(
        pickled_constants,
        archive_writer,
        constants_config,
        CONSTANTS_DIR,
        TENSOR_CONSTANT_FILENAME_PREFIX,
        tensor_idx,
        pickle_protocol,
    )

    # Save constants in raw bytes format
    _save_raw_tensors(
        raw_constants,
        model_name,
        archive_writer,
        constants_config,
        CONSTANTS_DIR,
        TENSOR_CONSTANT_FILENAME_PREFIX,
        tensor_idx,
    )

    # Handle custom objects
    for constant_fqn, constant in custom_objects:
        path_name = f"{CUSTOM_OBJ_FILENAME_PREFIX}{custom_obj_idx}"
        archive_path = os.path.join(CONSTANTS_DIR, path_name)
        custom_obj_bytes = torch._C._pickle_save(constant)
        archive_writer.write_bytes(archive_path, custom_obj_bytes)

        constants_config[constant_fqn] = schema.PayloadMeta(
            path_name=path_name,
            is_param=False,
            use_pickle=True,
            tensor_meta=None,
        )
        custom_obj_idx += 1

    return schema.PayloadConfig(config=constants_config)

