
def extend_user_visible_output_strides(
    user_visible_outputs: dict[Node, tuple[int, ...]],
) -> dict[Node, object]:
    """
    Extend user_visible_output_strides to include view ops that lead to user-visible outputs.
    """
    result: dict[Node, object] = {**user_visible_outputs}
    queue = [*result.keys()]
    visited = OrderedSet([*queue])
    while queue:
        current = queue.pop()
        if (
            _is_view_op(current.target)
            and current.args
            and isinstance(current.args[0], torch.fx.Node)
        ):
            base = current.args[0]
            if base not in visited:
                result.setdefault(base, None)
                visited.add(base)
                queue.append(base)
    return result

