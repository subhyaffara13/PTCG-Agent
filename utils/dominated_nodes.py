from typing import Any, Callable

def dominated_nodes(
    initial_queue: Iterable[torch.fx.Node],
    skip_filter: Callable[[Any], bool] | None = None,
) -> OrderedSet[torch.fx.Node]:
    """Returns the set of nodes whose values depend on those within initial_queue"""
    initial_queue = list(initial_queue)
    dominated_set = OrderedSet(initial_queue)

    while initial_queue:
        node = initial_queue.pop()
        for user in node.users:
            if skip_filter and skip_filter(user):
                continue
            if user not in dominated_set:
                dominated_set.add(user)
                initial_queue.append(user)

    return dominated_set

