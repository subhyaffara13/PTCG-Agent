
def count_lines(p):
    return sum(1 for _ in open(p, 'r', encoding='utf-8'))

