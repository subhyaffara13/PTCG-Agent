import os
import math


def _process_output_file(
    output_file: str,
    output_data: _OutputFileData,
    input_files_data: dict[str, _InputFileData],
) -> None:
    """
    Process a single output file by writing tensor data from input files using direct reads.

    This function is designed to be run in parallel for different output files.

    Args:
        output_file: Path to the output file
        output_data: Metadata for the output file
        input_files_data: Dictionary mapping input file paths to their metadata
    """

    sorted_tensors = sorted(
        output_data.fqn_data.items(), key=lambda x: x[1].offset_in_file
    )

    file_handles = {}
    dcp_metadata = {}
    for safetensors_file, file_data in input_files_data.items():
        dcp_metadata[safetensors_file] = _get_dcp_custom_metadata(file_data.metadata)

    try:
        # Open all input files for reading
        for safetensors_file in input_files_data:
            file_handles[safetensors_file] = open(safetensors_file, "rb")  # noqa: SIM115

        with open(output_file, "r+b") as output_stream:
            output_stream.seek(0, os.SEEK_END)
            # Process each tensor in sequential output order
            for tensor_fqn, tensor_fqn_data in sorted_tensors:
                full_tensor_mv = memoryview(
                    bytearray(
                        math.prod(tensor_fqn_data.shape_in_file)
                        * tensor_fqn_data.dtype_size
                    )
                )

                # Process each input safetensors file
                for safetensors_file in input_files_data:
                    file_metadata = input_files_data[safetensors_file].metadata
                    input_metadata_size = input_files_data[
                        safetensors_file
                    ].metadata_size

                    if tensor_fqn not in file_metadata:
                        continue

                    metadata = file_metadata[tensor_fqn]

                    data_offsets = metadata[DATA_OFFSETS_KEY]

                    # Use explicit reads to fetch tensor data efficiently
                    data_to_write = _read_tensor_data(
                        file_handles[safetensors_file],
                        data_offsets[0],
                        data_offsets[1],
                        input_metadata_size,
                    )

                    # Get the offsets of this tensor shard within the full tensor
                    # pyrefly: ignore [unsupported-operation]
                    fqn_custom_metadata = dcp_metadata[safetensors_file][tensor_fqn]  # type: ignore[index]
                    offsets_of_tensor_being_read = fqn_custom_metadata[
                        SAVED_OFFSETS_KEY
                    ]  # type: ignore[index]

                    # Write this tensor shard to the appropriate position in the output file
                    _write_sub_tensor_to_file_optimized(
                        full_tensor_mv,
                        data_to_write,
                        tensor_fqn_data.dtype_size,  # Size of each element in bytes
                        tensor_fqn_data.shape_in_file,  # Full tensor shape
                        offsets_of_tensor_being_read,  # Where this shard belongs in the full tensor
                        metadata[SHAPE_KEY],  # Shape of this shard
                    )

                output_stream.write(full_tensor_mv)

    finally:
        for f in file_handles.values():
            f.close()

