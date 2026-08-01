
def merge_sig_lines(lines, start):
    merged = ''
    paren_depth = 0
    i = start
    while i < len(lines):
        l = lines[i]
        clean = l.split('//')[0]
        merged += ' ' + clean.strip() if merged else clean.strip()
        for c in clean:
            if c == '(': paren_depth += 1
            elif c == ')': paren_depth -= 1
        if paren_depth == 0:
            if '{' in clean:
                return merged, i + 1
            next_i = i + 1
            while next_i < len(lines) and not lines[next_i].strip():
                next_i += 1
            if next_i < len(lines) and '{' in lines[next_i].split('//')[0]:
                merged += ' {\n'
                return merged, next_i + 1
        i += 1
    return None, len(lines)

