
def process_cache_map(
    parser: argparse.ArgumentParser, special_opts: argparse.Namespace, options: Options
) -> None:
    """Validate cache_map and copy into options.cache_map."""
    n = len(special_opts.cache_map)
    if n % 3 != 0:
        parser.error("--cache-map requires one or more triples (see source)")
    for i in range(0, n, 3):
        source, meta_file, data_file = special_opts.cache_map[i : i + 3]
        if source in options.cache_map:
            parser.error(f"Duplicate --cache-map source {source})")
        if not source.endswith(".py") and not source.endswith(".pyi"):
            parser.error(f"Invalid --cache-map source {source} (triple[0] must be *.py[i])")
        if not meta_file.endswith((".meta.json", ".meta.ff")):
            parser.error(
                "Invalid --cache-map meta_file %s (triple[1] must be *.meta.json or *.meta.ff)"
                % meta_file
            )
        if not data_file.endswith((".data.json", ".data.ff")):
            parser.error(
                "Invalid --cache-map data_file %s (triple[2] must be *.data.json or *.data.ff)"
                % data_file
            )
        options.cache_map[source] = (meta_file, data_file)

