
def is_ufunc_dispatch_key(dk: DispatchKey) -> bool:
    # For now, ufunc dispatch keys coincide with structured keys
    return dk in UFUNC_DISPATCH_KEYS

