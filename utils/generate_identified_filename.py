
def generate_identified_filename(filename: Path, identifier: str) -> Path:
    """
    Helper function to generate a identifiable filepath by concatenating the given identifier as a suffix.
    """
    return filename.parent.joinpath(filename.stem + identifier + filename.suffix)

