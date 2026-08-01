
def _validate_hashes(hashes: Mapping[str, Any]) -> Mapping[str, Any]:
    if not hashes:
        raise PylockValidationError("At least one hash must be provided")
    if not all(isinstance(hash_val, str) for hash_val in hashes.values()):
        raise PylockValidationError("Hash values must be strings")
    return hashes


def _validate_hashes(hashes: Mapping[str, Any]) -> Mapping[str, Any]:
    if not hashes:
        raise PylockValidationError("At least one hash must be provided")
    if not all(isinstance(hash_val, str) for hash_val in hashes.values()):
        raise PylockValidationError("Hash values must be strings")
    return hashes


def _validate_hashes(hashes: Mapping[str, Any]) -> Mapping[str, Any]:
    if not hashes:
        raise PylockValidationError("At least one hash must be provided")
    if not all(isinstance(hash_val, str) for hash_val in hashes.values()):
        raise PylockValidationError("Hash values must be strings")
    return hashes

