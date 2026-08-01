
def get_reachable_graph(root: object) -> tuple[dict[int, object], dict[int, tuple[int, object]]]:
    parents = {}
    seen = {id(root): root}
    worklist = [root]
    while worklist:
        o = worklist.pop()
        for s, e in get_edges(o):
            if id(e) in seen:
                continue
            parents[id(e)] = (id(o), s)
            seen[id(e)] = e
            worklist.append(e)

    return seen, parents

