import re

def _mock_expand_patterns(patterns, *_, **__):
    """
    Allow comparing the given patterns for 2 dist objects.
    We need to strip special chars to avoid errors when validating.
    """
    return [
        re.sub("[^a-z0-9]+", "", p, flags=re.IGNORECASE) or "empty" for p in patterns
    ]

