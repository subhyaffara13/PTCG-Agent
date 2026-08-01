
def sort_groups(groups):
    group_map = {group.name.lower(): group for group in groups}
    graph = {
        group.name.lower(): [
            x.group.lower()
            for x in _flatten_group(group)
            if isinstance(x, VAst.GroupName)
        ]
        for group in groups
    }
    sorter = TopologicalSorter(graph)
    return [group_map[name] for name in sorter.static_order()]

