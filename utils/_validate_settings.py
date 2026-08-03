import re

def _validate_settings(settings):
    return re.fullmatch(_gen_settings_regex(), settings) is not None

