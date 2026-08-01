
def apply_constraint(source, info, constraints, case_flags, saved_pos,
  sequence):
    element = sequence.pop()
    if element is None:
        raise error("nothing for fuzzy constraint", source.string, saved_pos)

    # If a group is marked as fuzzy then put all of the fuzzy part in the
    # group.
    if isinstance(element, Group):
        element.subpattern = Fuzzy(element.subpattern, constraints)
        sequence.append(element)
    else:
        sequence.append(Fuzzy(element, constraints))

