
def _register_fusion_pattern(pattern):
    def insert(fn):
        _DEFAULT_FUSION_PATTERNS[pattern] = fn
        return fn

    return insert

