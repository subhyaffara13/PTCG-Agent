
def filter_stack(stack: StackSummary) -> StackSummary:
    user_stack = StackSummary()
    for frame in stack:
        if frame.filename is None:
            continue
        if "convert_frame" in frame.filename:
            break
        if "eval_frame" in frame.filename or (
            frame.line and "torch._dynamo.optimize(" in frame.line
        ):
            continue
        user_stack.append(frame)

    return user_stack

