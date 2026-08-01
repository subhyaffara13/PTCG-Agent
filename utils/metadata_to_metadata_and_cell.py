
def metadata_to_metadata_and_cell(nb, metadata, fmt, unsupported_keys=None):
    # stash notebook metadata, including keys promoted to the root level
    metadata = recursive_update(
        metadata,
        filter_metadata(
            nb.metadata,
            fmt.get("root_level_metadata_filter", ""),
            default_root_level_metadata_filter(fmt),
            unsupported_keys=unsupported_keys,
            remove=True,
        ),
    )
    # move remaining metadata (i.e. frontmatter) to the first notebook cell
    if nb.metadata and fmt.get("root_level_metadata_as_raw_cell", True):
        frontmatter = yaml.safe_dump(nb.metadata, sort_keys=False)
        nb.cells.insert(0, new_raw_cell("---\n" + frontmatter + "---"))
    # attach the stashed metadata to notebook
    nb.metadata = metadata
    return nb

