
def _load_exported_programs(
    archive_reader: PT2ArchiveReader,
    file_names: list[str],
    expected_opset_version: dict[str, int] | None,
) -> dict[str, ExportedProgram]:
    exported_program_files = [
        file for file in file_names if file.startswith(MODELS_DIR)
    ]
    exported_programs = {}
    for file in exported_program_files:
        prefix, suffix = MODELS_FILENAME_FORMAT.split(
            "{}"
        )  # split "models/{}.json" into "models/" and "json"
        model_name = file[
            len(prefix) : -len(suffix)
        ]  # given "models/foo.json" we can now get "foo"

        sample_inputs_file = SAMPLE_INPUTS_FILENAME_FORMAT.format(model_name)
        serialized_sample_inputs = archive_reader.read_bytes(sample_inputs_file)

        from torch._export.serde.serialize import _bytes_to_dataclass

        exported_program_bytes = archive_reader.read_bytes(file)
        serialized_exported_program = _bytes_to_dataclass(
            schema.ExportedProgram, exported_program_bytes
        )
        state_dict = _load_state_dict(archive_reader, model_name)
        constants = _load_constants(archive_reader, model_name)

        ep = ExportedProgramDeserializer(expected_opset_version).deserialize(
            serialized_exported_program,
            state_dict,
            constants,
            serialized_sample_inputs,
        )

        exported_programs[model_name] = ep

    return exported_programs

