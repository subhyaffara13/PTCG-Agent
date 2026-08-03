import re

def _process_date_pattern(dp):
    """Compute a regex for each date pattern to use as a prefilter."""
    pattern, mask = dp
    regex = pattern
    regex = regex.replace(".", re.escape("."))
    regex = regex.replace("-", re.escape("-"))
    regex = regex.replace(" ", r"\s+")
    for field, field_regex in _FIELD_TO_REGEX:
        regex = regex.replace(field, field_regex)
    # Make sure we didn't miss any of the fields.
    assert "%" not in regex, regex
    return pattern, mask, re.compile("^" + regex + "$")

