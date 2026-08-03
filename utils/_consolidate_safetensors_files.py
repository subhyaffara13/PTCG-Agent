import os

def _consolidate_safetensors_files(
    input_dir: str,
    output_dir: str,
    fqn_to_file_mapping: dict[str, str],
    num_threads: int,
) -> dict[str, _OutputFileData]:
    output_files_data: dict[str, _OutputFileData] = {}
    # Create multiple output files based on the provided mapping
    for fqn, filename in fqn_to_file_mapping.items():
        output_path = os.path.join(output_dir, filename)

        if output_path not in output_files_data:
            output_files_data[output_path] = _OutputFileData(fqn_data={fqn: _FqnData()})
        else:
            output_files_data[output_path].fqn_data[fqn] = _FqnData()

    # Find all safetensors files in the input directory
    safetensors_files = glob.glob(os.path.join(input_dir, f"*{SUFFIX}"))

    # Read metadata from all input files
    input_files_data: dict[str, _InputFileData] = {}
    for safetensor_file in safetensors_files:
        with open(safetensor_file, "rb") as f:
            metadata, size = _get_safetensors_file_metadata(f)
            input_files_data[safetensor_file] = _InputFileData(
                metadata_size=size, metadata=metadata
            )
    # Step 1: Parse metadata to determine tensor shapes and types
    _parse_input_metadata(input_files_data, output_files_data)

    # Step 2: Write metadata headers to output files
    _write_metadata(output_files_data)
    # Step 3: Write actual tensor data from input files to output files
    _write_data(input_files_data, output_files_data, num_threads)

    return output_files_data

