
def compute_file_hash(path: Path, algorithm: HashAlgo) -> str:
    """
    Compute the checksum of a local file using the requested algorithm.
    """

    with path.open("rb") as stream:
        if algorithm == "sha256":
            return sha_fileobj(stream).hex()
        if algorithm == "git-sha1":
            return git_hash(stream.read())
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")

