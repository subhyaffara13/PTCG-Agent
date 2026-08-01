
def get_config_request_key(
    arch: str,
    toolkit_version: str,
    instantiation_level: str,
) -> str:
    """
    Return a key for the full ops, based on cutlass key, arch, toolkit version, instantiation level, and serialization.py file hash.
    """

    # Get hash of serialization.py and cutlass_utils.py files using their module file paths
    def get_file_hash(file_module):
        file_path = inspect.getfile(file_module)
        with open(file_path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()

    serialization_hash = get_file_hash(serialization)
    cutlass_utils_hash = get_file_hash(utils)

    hash_target = "-".join(
        [
            cutlass_key().hex(),
            arch,
            toolkit_version,
            instantiation_level,
            serialization_hash,
            cutlass_utils_hash,
        ]
    )
    return hashlib.sha256(hash_target.encode("utf-8")).hexdigest()[0:8]

