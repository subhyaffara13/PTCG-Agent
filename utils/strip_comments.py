import re

def strip_comments(s):
    return re.sub(r"\s+#.*", "", s)


def strip_comments(s):
    return '\n'.join(
        line
        for line in s.split('\n')
        if line.strip() and not line.strip().startswith('#')
    )

