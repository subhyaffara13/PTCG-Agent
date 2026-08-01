
def variadic_signature_matches(types, full_signature):
    # No arguments always matches a variadic signature
    if not full_signature:
        raise AssertionError("full_signature is empty")
    return all(variadic_signature_matches_iter(types, full_signature))

