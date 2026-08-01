
def _is_within(match, matches):
    for m in matches:
        if match.start() > m.start() and \
                match.end() < m.end():
            return True
    return False

