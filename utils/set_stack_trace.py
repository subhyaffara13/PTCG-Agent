
def set_stack_trace(stack: list[str]) -> None:
    global current_meta

    if should_preserve_node_meta:
        if stack:
            current_meta["stack_trace"] = "".join(stack)
        else:
            # when the stack is empty, we explicitly clear the stack_trace to avoid
            # propagating it to future node.˙
            current_meta.pop("stack_trace", None)

