
def _pylock_hashes_to_hash_options(hashes: Mapping[str, str]) -> dict[str, list[str]]:
    return {k: [v] for k, v in hashes.items()}

