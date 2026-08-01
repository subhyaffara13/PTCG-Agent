
def check_dependency(partition):
    """Given a partition,check if there is a circular dependency on
    this partition using bfs
    """
    visited: set[Partition] = {partition}
    queue: deque[Partition] = deque([partition])
    while queue:
        p = queue.popleft()
        for child in p.children:
            if child == partition:
                return True
            else:
                if child not in visited:
                    visited.add(child)
                    queue.append(child)
    return False

