
def git_hash(data: bytes) -> str:
    """
    Computes the git-sha1 hash of the given bytes, using the same algorithm as git.

    This is equivalent to running `git hash-object`. See https://git-scm.com/docs/git-hash-object
    for more details.

    Note: this method is valid for regular files. For LFS files, the proper git hash is supposed to be computed on the
          pointer file content, not the actual file content. However, for simplicity, we directly compare the sha256 of
          the LFS file content when we want to compare LFS files.

    Args:
        data (`bytes`):
            The data to compute the git-hash for.

    Returns:
        `str`: the git-hash of `data` as an hexadecimal string.

    Example:
    ```python
    >>> from huggingface_hub.utils.sha import git_hash
    >>> git_hash(b"Hello, World!")
    'b45ef6fec89518d314f546fd6c3025367b721684'
    ```
    """
    # Taken from https://gist.github.com/msabramo/763200
    # Note: no need to optimize by reading the file in chunks as we're not supposed to hash huge files (5MB maximum).
    sha = sha1()
    sha.update(b"blob ")
    sha.update(str(len(data)).encode())
    sha.update(b"\0")
    sha.update(data)
    return sha.hexdigest()

