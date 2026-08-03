import re

def _gen_settings_regex():
    return re.compile(r"((\+|-)?[\w\.]+,\s*)*(\+|-)?[\w\.]+?")

