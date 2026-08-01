
def _get_parquet_byte_ranges(
    paths,
    fs,
    metadata=None,
    columns=None,
    row_groups=None,
    max_gap=64_000,
    max_block=256_000_000,
    footer_sample_size=1_000_000,
    engine="auto",
    filters=None,
):
    """Get a dictionary of the known byte ranges needed
    to read a specific column/row-group selection from a
    Parquet dataset. Each value in the output dictionary
    is intended for use as the `data` argument for the
    `KnownPartsOfAFile` caching strategy of a single path.
    """

    # Set engine if necessary
    if isinstance(engine, str):
        engine = _set_engine(engine)

    # Pass to a specialized function if metadata is defined
    if metadata is not None:
        # Use the provided parquet metadata object
        # to avoid transferring/parsing footer metadata
        return _get_parquet_byte_ranges_from_metadata(
            metadata,
            fs,
            engine,
            columns=columns,
            row_groups=row_groups,
            max_gap=max_gap,
            max_block=max_block,
            filters=filters,
        )

    # Populate global paths, starts, & ends
    if columns is None and row_groups is None and filters is None:
        # We are NOT selecting specific columns or row-groups.
        #
        # We can avoid sampling the footers, and just transfer
        # all file data with cat_ranges
        result = {path: {(0, len(data)): data} for path, data in fs.cat(paths).items()}
    else:
        # We ARE selecting specific columns or row-groups.
        #
        # Get file sizes asynchronously
        file_sizes = fs.sizes(paths)
        data_paths = []
        data_starts = []
        data_ends = []
        # Gather file footers.
        # We just take the last `footer_sample_size` bytes of each
        # file (or the entire file if it is smaller than that)
        footer_starts = [
            max(0, file_size - footer_sample_size) for file_size in file_sizes
        ]
        footer_samples = fs.cat_ranges(paths, footer_starts, file_sizes)

        # Check our footer samples and re-sample if necessary.
        large_footer = []
        for i, path in enumerate(paths):
            footer_size = int.from_bytes(footer_samples[i][-8:-4], "little")
            real_footer_start = file_sizes[i] - (footer_size + 8)
            if real_footer_start < footer_starts[i]:
                large_footer.append((i, real_footer_start))
        if large_footer:
            warnings.warn(
                f"Not enough data was used to sample the parquet footer. "
                f"Try setting footer_sample_size >= {large_footer}."
            )
            path0 = [paths[i] for i, _ in large_footer]
            starts = [_[1] for _ in large_footer]
            ends = [file_sizes[i] - footer_sample_size for i, _ in large_footer]
            data = fs.cat_ranges(path0, starts, ends)
            for i, (path, start, block) in enumerate(zip(path0, starts, data)):
                footer_samples[i] = block + footer_samples[i]
                footer_starts[i] = start
        result = {
            path: {(start, size): data}
            for path, start, size, data in zip(
                paths, footer_starts, file_sizes, footer_samples
            )
        }

        # Calculate required byte ranges for each path
        for i, path in enumerate(paths):
            # Use "engine" to collect data byte ranges
            path_data_starts, path_data_ends = engine._parquet_byte_ranges(
                columns,
                row_groups=row_groups,
                footer=footer_samples[i],
                footer_start=footer_starts[i],
                filters=filters,
            )

            data_paths += [path] * len(path_data_starts)
            data_starts += path_data_starts
            data_ends += path_data_ends

        # Merge adjacent offset ranges
        data_paths, data_starts, data_ends = merge_offset_ranges(
            data_paths,
            data_starts,
            data_ends,
            max_gap=max_gap,
            max_block=max_block,
            sort=True,
        )

        # Transfer the data byte-ranges into local memory
        _transfer_ranges(fs, result, data_paths, data_starts, data_ends)

    # Add b"PAR1" to headers
    _add_header_magic(result)

    return result

