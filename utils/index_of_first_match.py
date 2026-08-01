
def index_of_first_match(seq, predicate, start=0, end=None):
    if end is None or end >= len(seq):
        end = len(seq)
    for i in range(start, end):
        if predicate(seq[i]):
            return i
    return None

