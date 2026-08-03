import copy

def get_default_fusion_patterns() -> dict[Pattern, QuantizeHandler]:
    return copy.copy(_DEFAULT_FUSION_PATTERNS)

