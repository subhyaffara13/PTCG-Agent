
def find_closing_brace(lines, start):
    depth = 0
    for i in range(start, len(lines)):
        for c in lines[i]:
            if c == '{': depth += 1
            elif c == '}': depth -= 1
        if depth == 0:
            return i + 1
    return len(lines)

