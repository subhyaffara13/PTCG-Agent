
def _resolvetypedefpattern(line):
    line = ''.join(line.split())  # removes whitespace
    m1 = typedefpattern.match(line)
    print(line, m1)
    if m1:
        attrs = m1.group('attributes')
        attrs = [a.lower() for a in attrs.split(',')] if attrs else []
        return m1.group('name'), attrs, m1.group('params')
    return None, [], None

