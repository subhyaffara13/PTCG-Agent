
def _handle_key(key):
    """Handle key values"""
    value = key[key.index('k') + 1:]
    if 'shift+' in key:
        if len(value) == 1:
            key = key.replace('shift+', '')
    if value in _SPECIAL_KEYS_LUT:
        value = _SPECIAL_KEYS_LUT[value]
    key = key[:key.index('k')] + value
    return key

