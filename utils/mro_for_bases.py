from typing import Any

def mro_for_bases(bases: tuple[type[Any], ...]) -> tuple[type[Any], ...]:
    def merge_seqs(seqs: list[deque[type[Any]]]) -> Iterable[type[Any]]:
        while True:
            non_empty = [seq for seq in seqs if seq]
            if not non_empty:
                # Nothing left to process, we're done.
                return
            candidate: type[Any] | None = None
            for seq in non_empty:  # Find merge candidates among seq heads.
                candidate = seq[0]
                not_head = [s for s in non_empty if candidate in islice(s, 1, None)]
                if not_head:
                    # Reject the candidate.
                    candidate = None
                else:
                    break
            if not candidate:
                raise TypeError('Inconsistent hierarchy, no C3 MRO is possible')
            yield candidate
            for seq in non_empty:
                # Remove candidate.
                if seq[0] == candidate:
                    seq.popleft()

    seqs = [deque(mro(base)) for base in bases] + [deque(bases)]
    return tuple(merge_seqs(seqs))

