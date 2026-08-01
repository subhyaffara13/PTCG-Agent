
def find_parents_and_order(glyphsets, locations, *, discrete_axes=set()):
    parents = [None] + list(range(len(glyphsets) - 1))
    order = list(range(len(glyphsets)))
    if locations:
        # Order base master first
        bases = [
            i
            for i, l in enumerate(locations)
            if all(v == 0 for k, v in l.items() if k not in discrete_axes)
        ]
        if bases:
            log.info("Found %s base masters: %s", len(bases), bases)
        else:
            log.warning("No base master location found")

        # Form a minimum spanning tree of the locations
        try:
            from scipy.sparse.csgraph import minimum_spanning_tree

            graph = [[0] * len(locations) for _ in range(len(locations))]
            axes = set()
            for l in locations:
                axes.update(l.keys())
            axes = sorted(axes)
            vectors = [tuple(l.get(k, 0) for k in axes) for l in locations]
            for i, j in itertools.combinations(range(len(locations)), 2):
                i_discrete_location = {
                    k: v for k, v in zip(axes, vectors[i]) if k in discrete_axes
                }
                j_discrete_location = {
                    k: v for k, v in zip(axes, vectors[j]) if k in discrete_axes
                }
                if i_discrete_location != j_discrete_location:
                    continue
                graph[i][j] = vdiff_hypot2(vectors[i], vectors[j])

            tree = minimum_spanning_tree(graph, overwrite=True)
            rows, cols = tree.nonzero()
            graph = defaultdict(set)
            for row, col in zip(rows, cols):
                graph[row].add(col)
                graph[col].add(row)

            # Traverse graph from the base and assign parents
            parents = [None] * len(locations)
            order = []
            visited = set()
            queue = deque(bases)
            while queue:
                i = queue.popleft()
                visited.add(i)
                order.append(i)
                for j in sorted(graph[i]):
                    if j not in visited:
                        parents[j] = i
                        queue.append(j)
            assert len(order) == len(
                parents
            ), "Not all masters are reachable; report an issue"

        except ImportError:
            pass

        log.info("Parents: %s", parents)
        log.info("Order: %s", order)
    return parents, order

