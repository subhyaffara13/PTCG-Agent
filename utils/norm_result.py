import re

def norm_result(result):
    "normalize differences, such as timing between output"
    for normalizer, replacement in NORMALIZERS:
        if hasattr(normalizer, "__call__"):
            result = normalizer(result)
        else:
            result = re.sub(normalizer, replacement, result)

    return result

