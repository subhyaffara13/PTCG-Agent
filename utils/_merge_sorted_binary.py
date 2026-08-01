
def _merge_sorted_binary(seqs):
    mid = len(seqs) // 2
    L1 = seqs[:mid]
    if len(L1) == 1:
        seq1 = iter(L1[0])
    else:
        seq1 = _merge_sorted_binary(L1)
    L2 = seqs[mid:]
    if len(L2) == 1:
        seq2 = iter(L2[0])
    else:
        seq2 = _merge_sorted_binary(L2)

    try:
        val2 = next(seq2)
    except StopIteration:
        yield from seq1
        return

    for val1 in seq1:
        if val2 < val1:
            yield val2
            for val2 in seq2:
                if val2 < val1:
                    yield val2
                else:
                    yield val1
                    break
            else:
                break
        else:
            yield val1
    else:
        yield val2
        yield from seq2
        return
    yield val1
    yield from seq1

