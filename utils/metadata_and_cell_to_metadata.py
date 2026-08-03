import logging

def metadata_and_cell_to_metadata(nb, fmt, unsupported_keys=None):
    # new metadata from filtered nb.metadata
    metadata = filter_metadata(
        nb.metadata,
        fmt.get("root_level_metadata_filter", ""),
        default_root_level_metadata_filter(fmt),
        unsupported_keys=unsupported_keys,
        remove=True,
    )
    # remaining nb.metadata moved under namespace key for jupyter metadata
    if nb.metadata:
        metadata[_JUPYTER_METADATA_NAMESPACE] = nb.metadata
    # move first cell frontmatter to the root level of nb.metadata (overwrites)
    if nb.cells and fmt.get("root_level_metadata_as_raw_cell", True):
        cell = nb.cells[0]
        if cell.cell_type == "raw":
            lines = cell.source.strip("\n\t ").splitlines()
            if len(lines) >= 2 and _HEADER_RE.match(lines[0]) and _HEADER_RE.match(lines[-1]):
                try:
                    frontmatter = next(yaml.safe_load_all(cell.source))
                except (yaml.parser.ParserError, yaml.scanner.ScannerError):
                    logging.warning("[jupytext] failed to parse YAML in raw cell")
                else:
                    if not isinstance(frontmatter, dict):
                        logging.warning("[jupytext] YAML header in raw cell is not a dictionary")
                    else:
                        nb.cells = nb.cells[1:]
                        if "root_level_metadata_filter" not in fmt and default_root_level_metadata_filter(fmt) == "all":
                            metadata.setdefault("jupytext", {})["root_level_metadata_filter"] = "-" + ",-".join(frontmatter)
                        metadata = recursive_update(frontmatter, metadata, overwrite=False)
    nb.metadata = metadata
    return nb

