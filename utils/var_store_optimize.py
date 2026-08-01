
def VarStore_optimize(self, use_NO_VARIATION_INDEX=True, quantization=1):
    """Optimize storage. Returns mapping from old VarIdxes to new ones."""

    # Overview:
    #
    # For each VarData row, we first extend it with zeroes to have
    # one column per region in VarRegionList. We then group the
    # rows into _Encoding objects, by their "characteristic" bitmap.
    # The characteristic bitmap is a binary number representing how
    # many bytes each column of the data takes up to encode. Each
    # column is encoded in four bits. For example, if a column has
    # only values in the range -128..127, it would only have a single
    # bit set in the characteristic bitmap for that column. If it has
    # values in the range -32768..32767, it would have two bits set.
    # The number of ones in the characteristic bitmap is the "width"
    # of the encoding.
    #
    # Each encoding as such has a number of "active" (ie. non-zero)
    # columns. The overhead of encoding the characteristic bitmap
    # is 10 bytes, plus 2 bytes per active column.
    #
    # When an encoding is merged into another one, if the characteristic
    # of the old encoding is a subset of the new one, then the overhead
    # of the old encoding is completely eliminated. However, each row
    # now would require more bytes to encode, to the tune of one byte
    # per characteristic bit that is active in the new encoding but not
    # in the old one.
    #
    # The "gain" of merging two encodings is how many bytes we save by doing so.
    #
    # High-level algorithm:
    #
    # - Each encoding has a minimal way to encode it. However, because
    #   of the overhead of encoding the characteristic bitmap, it may
    #   be beneficial to merge two encodings together, if there is
    #   gain in doing so. As such, we need to search for the best
    #   such successive merges.
    #
    # Algorithm:
    #
    # - Put all encodings into a "todo" list.
    #
    # - Sort todo list (for stability) by width_sort_key(), which is a tuple
    #   of the following items:
    #   * The "width" of the encoding.
    #   * The characteristic bitmap of the encoding, with higher-numbered
    #     columns compared first.
    #
    # - Make a priority-queue of the gain from combining each two
    #   encodings in the todo list. The priority queue is sorted by
    #   decreasing gain. Only positive gains are included.
    #
    # - While priority queue is not empty:
    #   - Pop the first item from the priority queue,
    #   - Merge the two encodings it represents,
    #   - Remove the two encodings from the todo list,
    #   - Insert positive gains from combining the new encoding with
    #     all existing todo list items into the priority queue,
    #   - If a todo list item with the same characteristic bitmap as
    #     the new encoding exists, remove it from the todo list and
    #     merge it into the new encoding.
    #   - Insert the new encoding into the todo list,
    #
    # - Encode all remaining items in the todo list.
    #
    # The output is then sorted for stability, in the following way:
    # - The VarRegionList of the input is kept intact.
    # - The VarData is sorted by the same width_sort_key() used at the beginning.
    # - Within each VarData, the items are sorted as vectors of numbers.
    #
    # Finally, each VarData is optimized to remove the empty columns and
    # reorder columns as needed.

    # TODO
    # Check that no two VarRegions are the same; if they are, fold them.

    n = len(self.VarRegionList.Region)  # Number of columns
    zeroes = [0] * n

    front_mapping = {}  # Map from old VarIdxes to full row tuples

    encodings = _EncodingDict()

    # Collect all items into a set of full rows (with lots of zeroes.)
    for major, data in enumerate(self.VarData):
        regionIndices = data.VarRegionIndex

        for minor, item in enumerate(data.Item):
            row = list(zeroes)

            if quantization == 1:
                for regionIdx, v in zip(regionIndices, item):
                    row[regionIdx] += v
            else:
                for regionIdx, v in zip(regionIndices, item):
                    row[regionIdx] += (
                        round(v / quantization) * quantization
                    )  # TODO https://github.com/fonttools/fonttools/pull/3126#discussion_r1205439785

            row = tuple(row)

            if use_NO_VARIATION_INDEX and not any(row):
                front_mapping[(major << 16) + minor] = None
                continue

            encodings.add_row(row)
            front_mapping[(major << 16) + minor] = row

    # Prepare for the main algorithm.
    todo = sorted(encodings.values(), key=_Encoding.width_sort_key)
    del encodings

    # Repeatedly pick two best encodings to combine, and combine them.

    heap = []
    for i, encoding in enumerate(todo):
        for j in range(i + 1, len(todo)):
            other_encoding = todo[j]
            combining_gain = encoding.gain_from_merging(other_encoding)
            if combining_gain > 0:
                heappush(heap, (-combining_gain, i, j))

    while heap:
        _, i, j = heappop(heap)
        if todo[i] is None or todo[j] is None:
            continue

        encoding, other_encoding = todo[i], todo[j]
        todo[i], todo[j] = None, None

        # Combine the two encodings
        combined_chars = other_encoding.chars | encoding.chars
        combined_encoding = _Encoding(combined_chars)
        combined_encoding.extend(encoding.items)
        combined_encoding.extend(other_encoding.items)

        for k, enc in enumerate(todo):
            if enc is None:
                continue

            # In the unlikely event that the same encoding exists already,
            # combine it.
            if enc.chars == combined_chars:
                combined_encoding.extend(enc.items)
                todo[k] = None
                continue

            combining_gain = combined_encoding.gain_from_merging(enc)
            if combining_gain > 0:
                heappush(heap, (-combining_gain, k, len(todo)))

        todo.append(combined_encoding)

    encodings = [encoding for encoding in todo if encoding is not None]

    # Assemble final store.
    back_mapping = {}  # Mapping from full rows to new VarIdxes
    encodings.sort(key=_Encoding.width_sort_key)
    self.VarData = []
    for encoding in encodings:
        items = sorted(encoding.items)

        while items:
            major = len(self.VarData)
            data = ot.VarData()
            self.VarData.append(data)
            data.VarRegionIndex = range(n)
            data.VarRegionCount = len(data.VarRegionIndex)

            # Each major can only encode up to 0xFFFF entries.
            data.Item, items = items[:0xFFFF], items[0xFFFF:]

            for minor, item in enumerate(data.Item):
                back_mapping[item] = (major << 16) + minor

    # Compile final mapping.
    varidx_map = {NO_VARIATION_INDEX: NO_VARIATION_INDEX}
    for k, v in front_mapping.items():
        varidx_map[k] = back_mapping[v] if v is not None else NO_VARIATION_INDEX

    # Recalculate things and go home.
    self.VarRegionList.RegionCount = len(self.VarRegionList.Region)
    self.VarDataCount = len(self.VarData)
    for data in self.VarData:
        data.ItemCount = len(data.Item)
        data.optimize()

    # Remove unused regions.
    self.prune_regions()

    return varidx_map

