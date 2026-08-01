
def _get_post_order_named_modules(
    root_module: nn.Module,
) -> list[tuple[str, nn.Module]]:
    """
    This returns the named modules following a post-order traversal, which is a
    valid reverse topological sort. We achieve this using the reverse of a
    stack-based DFS order instead of reversing ``root_module.named_modules()``
    since the former gives the modules in registration order at each level in
    the module tree (as opposed to the reverse), which allows us to error/warn
    on the first registered module that violates the condition.

    For example, consider the following module structure:
        M(
          S1(),
          S2(
            SS1(),
            SS2(),
          ),
          S3(),
        )
    The reverse DFS order is [S1, SS1, SS2, S2, S3, M], while the reverse
    ``named_modules()`` order is [S3, SS2, SS1, S2, S1, M].
    """
    visited_modules = {root_module}
    stack = [("", root_module)]
    # Append and reverse at the end for linear-time algorithm
    reverse_post_order_named_modules: list[tuple[str, nn.Module]] = []
    while stack:
        module_name, module = stack.pop()
        reverse_post_order_named_modules.append((module_name, module))
        for child_module_name, child_module in module.named_children():
            if child_module is None:  # only for overrides of `named_children()`
                continue
            if child_module not in visited_modules:
                visited_modules.add(child_module)
                if module_name != "":
                    child_module_name = module_name + "." + child_module_name
                stack.append((child_module_name, child_module))
    post_order_named_modules = list(reversed(reverse_post_order_named_modules))
    return post_order_named_modules

