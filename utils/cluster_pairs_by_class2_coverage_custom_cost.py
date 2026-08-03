from typing import Dict, List, Tuple

def cluster_pairs_by_class2_coverage_custom_cost(
    font: TTFont,
    pairs: Pairs,
    compression: int = 5,
) -> List[Pairs]:
    if not pairs:
        # The subtable was actually empty?
        return [pairs]

    # Sorted for reproducibility/determinism
    all_class1 = sorted(set(pair[0] for pair in pairs))
    all_class2 = sorted(set(pair[1] for pair in pairs))

    # Use Python's big ints for binary vectors representing each line
    lines = [
        sum(
            1 << i if (class1, class2) in pairs else 0
            for i, class2 in enumerate(all_class2)
        )
        for class1 in all_class1
    ]

    # Map glyph names to ids and work with ints throughout for ClassDef formats
    name_to_id = font.getReverseGlyphMap()
    # Each entry in the arrays below is (range_count, min_glyph_id, max_glyph_id)
    all_class1_data = [
        _getClassRanges(name_to_id[name] for name in cls) for cls in all_class1
    ]
    all_class2_data = [
        _getClassRanges(name_to_id[name] for name in cls) for cls in all_class2
    ]

    format1 = 0
    format2 = 0
    for pair, value in pairs.items():
        format1 |= value[0].getEffectiveFormat() if value[0] else 0
        format2 |= value[1].getEffectiveFormat() if value[1] else 0
    valueFormat1_bytes = bit_count(format1) * 2
    valueFormat2_bytes = bit_count(format2) * 2

    ctx = ClusteringContext(
        lines,
        all_class1,
        all_class1_data,
        all_class2_data,
        valueFormat1_bytes,
        valueFormat2_bytes,
    )

    cluster_cache: Dict[int, Cluster] = {}

    def make_cluster(indices: int) -> Cluster:
        cluster = cluster_cache.get(indices, None)
        if cluster is not None:
            return cluster
        cluster = Cluster(ctx, indices)
        cluster_cache[indices] = cluster
        return cluster

    def merge(cluster: Cluster, other: Cluster) -> Cluster:
        return make_cluster(cluster.indices_bitmask | other.indices_bitmask)

    # Agglomerative clustering by hand, checking the cost gain of the new
    # cluster against the previously separate clusters
    # Start with 1 cluster per line
    # cluster = set of lines = new subtable
    clusters = [make_cluster(1 << i) for i in range(len(lines))]

    # Cost of 1 cluster with everything
    # `(1 << len) - 1` gives a bitmask full of 1's of length `len`
    cost_before_splitting = make_cluster((1 << len(lines)) - 1).cost
    log.debug(f"        len(clusters) = {len(clusters)}")

    while len(clusters) > 1:
        lowest_cost_change = None
        best_cluster_index = None
        best_other_index = None
        best_merged = None
        for i, cluster in enumerate(clusters):
            for j, other in enumerate(clusters[i + 1 :]):
                merged = merge(cluster, other)
                cost_change = merged.cost - cluster.cost - other.cost
                if lowest_cost_change is None or cost_change < lowest_cost_change:
                    lowest_cost_change = cost_change
                    best_cluster_index = i
                    best_other_index = i + 1 + j
                    best_merged = merged
        assert lowest_cost_change is not None
        assert best_cluster_index is not None
        assert best_other_index is not None
        assert best_merged is not None

        # If the best merge we found is still taking down the file size, then
        # there's no question: we must do it, because it's beneficial in both
        # ways (lower file size and lower number of subtables).  However, if the
        # best merge we found is not reducing file size anymore, then we need to
        # look at the other stop criteria = the compression factor.
        if lowest_cost_change > 0:
            # Stop critera: check whether we should keep merging.
            # Compute size reduction brought by splitting
            cost_after_splitting = sum(c.cost for c in clusters)
            # size_reduction so that after = before * (1 - size_reduction)
            # E.g. before = 1000, after = 800, 1 - 800/1000 = 0.2
            size_reduction = 1 - cost_after_splitting / cost_before_splitting

            # Force more merging by taking into account the compression number.
            # Target behaviour: compression number = 1 to 9, default 5 like gzip
            #   - 1 = accept to add 1 subtable to reduce size by 50%
            #   - 5 = accept to add 5 subtables to reduce size by 50%
            # See https://github.com/harfbuzz/packtab/blob/master/Lib/packTab/__init__.py#L690-L691
            # Given the size reduction we have achieved so far, compute how many
            # new subtables are acceptable.
            max_new_subtables = -log2(1 - size_reduction) * compression
            log.debug(
                f"            len(clusters) = {len(clusters):3d}    size_reduction={size_reduction:5.2f}    max_new_subtables={max_new_subtables}",
            )
            if compression == 9:
                # Override level 9 to mean: create any number of subtables
                max_new_subtables = len(clusters)

            # If we have managed to take the number of new subtables below the
            # threshold, then we can stop.
            if len(clusters) <= max_new_subtables + 1:
                break

        # No reason to stop yet, do the merge and move on to the next.
        del clusters[best_other_index]
        clusters[best_cluster_index] = best_merged

    # All clusters are final; turn bitmasks back into the "Pairs" format
    pairs_by_class1: Dict[Tuple[str, ...], Pairs] = defaultdict(dict)
    for pair, values in pairs.items():
        pairs_by_class1[pair[0]][pair] = values
    pairs_groups: List[Pairs] = []
    for cluster in clusters:
        pairs_group: Pairs = dict()
        for i in cluster.indices:
            class1 = all_class1[i]
            pairs_group.update(pairs_by_class1[class1])
        pairs_groups.append(pairs_group)
    return pairs_groups

