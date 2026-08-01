
def _write_metadata(
    output_files_data: dict[str, _OutputFileData],
) -> None:
    """
    Write metadata to the beginning of each output safetensors file.

    This function writes the metadata section to each output file, including information
    about tensor shapes, data types, and offsets. It also updates the offset_in_file
    field for each tensor in the output_files_data.

    Args:
        output_files_data: Dictionary mapping output file paths to their metadata
    """
    # Process each output file
    for file_path, output_data in output_files_data.items():
        with open(file_path, "wb") as f:
            metadata = {}
            curr_offset = 0

            # Calculate offsets for each tensor in the file
            for fqn, fqn_data in output_data.fqn_data.items():
                # Calculate the end offset by multiplying all dimensions and the data type size
                end_offset = (
                    curr_offset
                    + math.prod(fqn_data.shape_in_file) * fqn_data.dtype_size
                )

                # Store metadata for this tensor
                metadata[fqn] = {
                    SHAPE_KEY: fqn_data.shape_in_file,
                    DTYPE_KEY: fqn_data.dtype_str,
                    DATA_OFFSETS_KEY: [
                        curr_offset,
                        end_offset,
                    ],  # Start and end byte offsets
                }
                # Store the offset for later use when writing the actual tensor data
                fqn_data.offset_in_file = curr_offset

                # Update current offset for the next tensor
                curr_offset = end_offset

            # Convert metadata to JSON and encode as bytes
            json_metadata = json.dumps(metadata)
            json_bytes = json_metadata.encode("utf-8")

            # Write the metadata size as an 8-byte unsigned integer (little-endian)
            size_in_bytes = len(json_bytes)
            header_len = struct.pack("<Q", size_in_bytes)

            # Write the header length and metadata to the file
            f.write(header_len)
            f.write(json_bytes)

            # Store the total metadata size (header + JSON) for later use
            output_data.metadata_size = f.tell()

