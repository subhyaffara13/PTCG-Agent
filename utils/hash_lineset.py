
def hash_lineset(
    lineset: LineSet, min_common_lines: int = DEFAULT_MIN_SIMILARITY_LINE
) -> tuple[HashToIndex_T, IndexToLines_T]:
    """Return two dicts.

    The first associates the hash of successive stripped lines of a lineset
    to the indices of the starting lines.
    The second dict, associates the index of the starting line in the lineset's stripped lines to the
    couple [start, end] lines number in the corresponding file.

    :param lineset: lineset object (i.e the lines in a file)
    :param min_common_lines: number of successive lines that are used to compute the hash
    :return: a dict linking hashes to corresponding start index and a dict that links this
             index to the start and end lines in the file
    """
    hash2index = defaultdict(list)
    index2lines = {}
    # Comments, docstring and other specific patterns maybe excluded -> call to stripped_lines
    # to get only what is desired
    lines = tuple(x.text for x in lineset.stripped_lines)
    # Need different iterators on same lines but each one is shifted 1 from the precedent
    shifted_lines = [iter(lines[i:]) for i in range(min_common_lines)]

    for i, *succ_lines in enumerate(zip(*shifted_lines)):
        start_linenumber = LineNumber(lineset.stripped_lines[i].line_number)
        try:
            end_linenumber = lineset.stripped_lines[i + min_common_lines].line_number
        except IndexError:
            end_linenumber = LineNumber(lineset.stripped_lines[-1].line_number + 1)

        index = Index(i)
        index2lines[index] = SuccessiveLinesLimits(
            start=start_linenumber, end=end_linenumber
        )

        l_c = LinesChunk(lineset.name, index, *succ_lines)
        hash2index[l_c].append(index)

    return hash2index, index2lines

