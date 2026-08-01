
def backtickrepl(m):
    if m.group('s'):
        return (f"with bounds ``{m.group('b')}`` with ``{m.group('s')}`` storage\n")
    else:
        return f"with bounds ``{m.group('b')}``\n"

