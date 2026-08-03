import re

def _egg_fragment(url):
    _egg_fragment_re = re.compile(r"[#&]egg=([^&]*)")
    match = _egg_fragment_re.search(url)
    if not match:
        return None
    return match.group(1)

