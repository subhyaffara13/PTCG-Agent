import re

def get_comment(ext):
    return re.escape(_SCRIPT_EXTENSIONS[ext]["comment"])

