
def consolidate_safetensors_files(
    input_dir: str,
    output_dir: str,
    fqn_to_index_mapping: dict[str, int],
    num_threads: int = 1,
) -> None:
    """
    Main function to consolidate sharded safetensors files into one or more output files.

    This function orchestrates the entire consolidation process:
    1. Sets up the output file structure based on the fqn_to_index_mapping
    2. Finds all safetensors files in the input directory
    3. Parses metadata from all input files
    4. Writes metadata to the output files
    5. Writes tensor data from input files to output files
    6. Writes overall model.index.safetensors.json file with weight map

    Args:
        input_dir: Directory containing sharded safetensors files
        output_dir: Directory where consolidated files will be written
        fqn_to_index_mapping: Optional mapping of tensor names to output file indices.
                             If None, all tensors will be consolidated into a single file.
        num_threads: Number of threads to use for parallel processing of saving data to output files.
    """
    start_time = time.time()
    logger.info(
        "Consolidating safetensors files from %s to %s. Beginning at time %f",
        input_dir,
        output_dir,
        start_time,
    )

    max_index = max(fqn_to_index_mapping.values())
    fqn_to_file_mapping = {
        fqn: _gen_file_name(idx, max_index) for fqn, idx in fqn_to_index_mapping.items()
    }

    output_files_data = _consolidate_safetensors_files(
        input_dir, output_dir, fqn_to_file_mapping, num_threads
    )

    # Step 4: Write overall model.index.safetensors.json file with weight map
    _write_overall_metadata_file(output_dir, output_files_data)

    logger.info("Done consolidating. Took %.2f secs.", time.time() - start_time)

