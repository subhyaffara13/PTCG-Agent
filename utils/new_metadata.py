
def new_metadata(
    name=None,
    authors=None,
    license=None,
    created=None,
    modified=None,
    gistid=None,
):
    """Create a new metadata node."""
    metadata = NotebookNode()
    if name is not None:
        metadata.name = str(name)
    if authors is not None:
        metadata.authors = list(authors)
    if created is not None:
        metadata.created = str(created)
    if modified is not None:
        metadata.modified = str(modified)
    if license is not None:
        metadata.license = str(license)
    if gistid is not None:
        metadata.gistid = str(gistid)
    return metadata


def new_metadata(
    name=None,
    authors=None,
    license=None,
    created=None,
    modified=None,
    gistid=None,
):
    """Create a new metadata node."""
    metadata = NotebookNode()
    if name is not None:
        metadata.name = str_passthrough(name)
    if authors is not None:
        metadata.authors = list(authors)
    if created is not None:
        metadata.created = str_passthrough(created)
    if modified is not None:
        metadata.modified = str_passthrough(modified)
    if license is not None:
        metadata.license = str_passthrough(license)
    if gistid is not None:
        metadata.gistid = str_passthrough(gistid)
    return metadata

