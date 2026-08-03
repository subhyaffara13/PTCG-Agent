import re

def apply_print_resets(buf):
    return re.sub(r"^.*\r", "", buf, 0, re.MULTILINE)

