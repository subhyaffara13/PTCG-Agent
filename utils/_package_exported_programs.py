
def _package_exported_programs(
    archive_writer: PT2ArchiveWriter,
    exported_programs: ExportedProgram | dict[str, ExportedProgram] | None,
    opset_version: dict[str, int] | None = None,
    pickle_protocol: int = DEFAULT_PICKLE_PROTOCOL,
) -> None:
    if exported_programs is None:
        return

    if isinstance(exported_programs, ExportedProgram):
        exported_programs = {"model": exported_programs}

    if not isinstance(exported_programs, dict):
        raise AssertionError(
            f"Expected exported_programs to be a dict, but got {type(exported_programs)}"
        )

    for model_name, ep in exported_programs.items():
        weights_config = _package_state_dict(
            model_name, ep, archive_writer, pickle_protocol
        )
        weights_config_file = WEIGHTS_CONFIG_FILENAME_FORMAT.format(model_name)
        _package_payload_config(archive_writer, weights_config, weights_config_file)

        constants_config = _package_constants(
            model_name, ep, archive_writer, pickle_protocol
        )
        constants_config_file = CONSTANTS_CONFIG_FILENAME_FORMAT.format(model_name)
        _package_payload_config(archive_writer, constants_config, constants_config_file)

        artifact: SerializedArtifact = serialize(
            ep,
            opset_version,
            pickle_protocol,
            serialize_state_dict=False,
            serialize_constants=False,
        )

        archive_writer.write_bytes(
            MODELS_FILENAME_FORMAT.format(model_name), artifact.exported_program
        )
        archive_writer.write_bytes(
            SAMPLE_INPUTS_FILENAME_FORMAT.format(model_name),
            artifact.example_inputs,
        )

