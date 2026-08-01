
def _resolvenameargspattern(line):
    line, bind_cname = parse_name_for_bind(line)
    line = markouterparen(line)
    m1 = nameargspattern.match(line)
    if m1:
        return m1.group('name'), m1.group('args'), m1.group('result'), bind_cname
    m1 = operatorpattern.match(line)
    if m1:
        name = m1.group('scheme') + '(' + m1.group('name') + ')'
        return name, [], None, None
    m1 = callnameargspattern.match(line)
    if m1:
        return m1.group('name'), m1.group('args'), None, None
    return None, [], None, None

