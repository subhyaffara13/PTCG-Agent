import re

def _collapse_verbose_regex(regex_str: str) -> str:
    if "\n" not in regex_str:
        return regex_str
    collapsed = pyparsing.Regex(r"#.*$").suppress().transform_string(regex_str)
    collapsed = re.sub(r"\s*\n\s*", "", collapsed)
    return collapsed

