
def read_cell_metadata(token, cell_index):
    """Return cell metadata"""
    metadata = {}
    if token.content:
        try:
            metadata = json.loads(token.content.strip())
        except Exception as err:
            raise MystMetadataParsingError(f"Markdown cell {cell_index} at line {token.map[0] + 1} could not be read: {err}")
        if not isinstance(metadata, dict):
            raise MystMetadataParsingError(f"Markdown cell {cell_index} at line {token.map[0] + 1} is not a dict")

    return metadata

