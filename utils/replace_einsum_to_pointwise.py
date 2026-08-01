
def replace_einsum_to_pointwise(match: Match, *args, **kwargs):
    def repl(input, weights):
        return (input.unsqueeze(-1) * weights).sum(-2)

    def should_replace_einsum(einsum_node) -> bool:
        equation = get_arg_value(einsum_node, 0)
        users = einsum_node.users.keys()
        # for now, we only consider the case of two operands
        return (
            len(einsum_node.args) == 3
            and is_node_meta_valid(input)
            and is_node_meta_valid(weights)
            and any(
                user.target == "add" or user.target is operator.add for user in users
            )
            and match_einsum_strings(equation)
        )

    einsum_node = match.nodes[0]
    input, weights = get_arg_value(einsum_node, 1), get_arg_value(einsum_node, 2)
    if should_replace_einsum(einsum_node):
        # pyrefly: ignore [bad-argument-type]
        match.replace_by_example(repl, [input, weights])
        counters[backend]["einsum_to_pointwise_pass"] += 1

