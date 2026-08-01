
def _add_mutation_dependencies(
    node_to_mutated_arg_positions: dict[Node, OrderedSet[int]],
    node_to_additional_deps: dict[Node, OrderedSet[Node]],
) -> None:
    for node, indices in node_to_mutated_arg_positions.items():
        flat_args_kwargs = _get_flat_args(node, {})

        # for all mutated args,
        # add dependency on usages which occur after node to ensure
        # node will always be ordered before them
        # also add node as a dependency on usages which
        # occur before node to ensure node is ordered after them
        for index in indices:
            mutated_arg = flat_args_kwargs[index]
            for user in mutated_arg.users:
                if user is node:
                    continue

                elif user < node:
                    node_to_additional_deps[node].add(user)

                elif user > node:
                    node_to_additional_deps[user].add(node)

