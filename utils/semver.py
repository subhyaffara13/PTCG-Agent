import re

def semver(v):
    if not re.fullmatch(r'\d+\.\d+\.\d+', v):
        raise ValueError
    return v

