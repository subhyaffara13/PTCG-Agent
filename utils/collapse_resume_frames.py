
def collapse_resume_frames(stack: StackSummary | list[FrameSummary]) -> StackSummary:
    """
    When we graph break, we create a resume function and make a regular Python call
    to it, which gets intercepted by Dynamo. This behavior is normally shown in the
    traceback, which can be confusing to a user. So we can filter out resume frames
    for better traceback clarity.

    Example:
    File "..." line 3, in f
        <line 3>
    File "..." line 5, in torch_dynamo_resume_in_f_at_80
        <line 5>
    File "..." line 10, in torch_dynamo_resume_in_f_at_120
        <line 10>

    becomes
    File "..." line 10, in f
        <line 10>
    """

    new_stack = StackSummary()
    for frame in stack:
        if frame.filename is None:
            continue
        name = remove_resume_prefix(frame.name)
        if new_stack and name and new_stack[-1].name == name:
            new_stack[-1] = frame
            frame.name = name
        else:
            frame.name = name
            new_stack.append(frame)

    return new_stack

