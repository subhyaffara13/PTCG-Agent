
def apply_quantifier(source, info, counts, case_flags, ch, saved_pos,
  sequence):
    element = sequence.pop()
    if element is None:
        if sequence:
            raise error("multiple repeat", source.string, saved_pos)
        raise error("nothing to repeat", source.string, saved_pos)

    if isinstance(element, (GreedyRepeat, LazyRepeat, PossessiveRepeat)):
        raise error("multiple repeat", source.string, saved_pos)

    min_count, max_count = counts
    saved_pos = source.pos
    ch = source.get()
    if ch == "?":
        # The "?" suffix that means it's a lazy repeat.
        repeated = LazyRepeat
    elif ch == "+":
        # The "+" suffix that means it's a possessive repeat.
        repeated = PossessiveRepeat
    else:
        # No suffix means that it's a greedy repeat.
        source.pos = saved_pos
        repeated = GreedyRepeat

    # Ignore the quantifier if it applies to a zero-width item or the number of
    # repeats is fixed at 1.
    if not element.is_empty() and (min_count != 1 or max_count != 1):
        element = repeated(element, min_count, max_count)

    sequence.append(element)

