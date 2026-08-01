
def _write_data(
    input_files_data: dict[str, _InputFileData],
    output_files_data: dict[str, _OutputFileData],
    num_threads: int = 1,
) -> None:
    """
    Write tensor data from input files to the output files using memory mapping.

    This function reads tensor data from each input file and writes it to the appropriate
    position in the output files based on the tensor's offsets. When num_threads > 1,
    the work is split across threads with each thread handling a different output file.

    Args:
        input_files_data: Dictionary mapping input file paths to their metadata
        output_files_data: Dictionary mapping output file paths to their metadata
        num_threads: Number of threads to use for parallel processing
    """
    if num_threads <= 1 or len(output_files_data) <= 1:
        # Sequential processing
        for output_file, output_data in output_files_data.items():
            _process_output_file(output_file, output_data, input_files_data)
    else:
        # Parallel processing with ThreadPoolExecutor
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=min(num_threads, len(output_files_data))
        ) as executor:
            futures = []
            for output_file, output_data in output_files_data.items():
                futures.append(
                    executor.submit(
                        _process_output_file,
                        output_file,
                        output_data,
                        input_files_data,
                    )
                )

            # Wait for all futures to complete
            for future in concurrent.futures.as_completed(futures):
                # Handle any exceptions that might have occurred
                try:
                    future.result()
                except Exception as e:
                    print(f"Error processing output file: {e}")
                    raise


def _write_data(m, fid, header):
    m = m.tocsc(copy=False)

    def write_array(f, ar, nlines, fmt):
        # ar_nlines is the number of full lines, n is the number of items per
        # line, ffmt the fortran format
        pyfmt = fmt.python_format
        pyfmt_full = pyfmt * fmt.repeat

        # for each array to write, we first write the full lines, and special
        # case for partial line
        full = ar[:(nlines - 1) * fmt.repeat]
        for row in full.reshape((nlines-1, fmt.repeat)):
            f.write(pyfmt_full % tuple(row) + "\n")
        nremain = ar.size - full.size
        if nremain > 0:
            f.write((pyfmt * nremain) % tuple(ar[ar.size - nremain:]) + "\n")

    fid.write(header.dump())
    fid.write("\n")
    # +1 is for Fortran one-based indexing
    write_array(fid, m.indptr+1, header.pointer_nlines,
                header.pointer_format)
    write_array(fid, m.indices+1, header.indices_nlines,
                header.indices_format)
    write_array(fid, m.data, header.values_nlines,
                header.values_format)

