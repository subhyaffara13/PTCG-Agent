
def parse_name_for_bind(line):
    pattern = re.compile(r'bind\(\s*(?P<lang>[^,]+)(?:\s*,\s*name\s*=\s*["\'](?P<name>[^"\']+)["\']\s*)?\)', re.I)
    match = pattern.search(line)
    bind_statement = None
    if match:
        bind_statement = match.group(0)
        # Remove the 'bind' construct from the line.
        line = line[:match.start()] + line[match.end():]
    return line, bind_statement

