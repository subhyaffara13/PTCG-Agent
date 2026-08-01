
def sync_state(*wrapped_method_modules):
    """
    Sync state between exported modules corresponding to wrapped methods.
    This might be necessary after serializing/deserializing due to copying.
    """
    if wrapped_method_modules:
        m, *other_ms = wrapped_method_modules
        for other_m in other_ms:
            _sync_state(m, other_m)

