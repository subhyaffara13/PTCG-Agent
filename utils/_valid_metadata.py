
def _valid_metadata(text: str) -> bool:
    metadata = Metadata.from_email(text, validate=True)  # can raise exceptions
    return metadata is not None

