
def are_argument_counts_overlapping(t: CallableType, s: CallableType) -> bool:
    """Can a single call match both t and s, based just on positional argument counts?"""
    min_args = max(t.min_args, s.min_args)
    max_args = min(t.max_possible_positional_args(), s.max_possible_positional_args())
    return min_args <= max_args

