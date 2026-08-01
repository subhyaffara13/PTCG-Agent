
def serialize_regexes(patterns_dict):
    # Unfortunately using `pprint.pformat` is causing errors
    # specially with big regexes
    regex_patterns = (
        repr(k) + ": " + repr_regex(v)
        for k, v in patterns_dict.items()
    )
    return '{\n    ' + ",\n    ".join(regex_patterns) + "\n}"

