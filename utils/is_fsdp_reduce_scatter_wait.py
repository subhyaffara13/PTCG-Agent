
def is_fsdp_reduce_scatter_wait(wait: torch.fx.Node) -> bool:
    if is_graph_output(wait):
        return True

    if len(wait.users) == 1:
        user = next(iter(wait.users))
        assert user is not None
        return (
            is_graph_output(user)
            and user.op == "call_function"
            and user.target is torch.ops.prims.convert_element_type.default
        )

    return False

